from django.http import JsonResponse
from django.urls import resolve
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
import re
import html
import json
from django.core.serializers.json import DjangoJSONEncoder

User = get_user_model()

class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Security Headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
        response['Content-Security-Policy'] = "default-src 'self'; img-src 'self' data: https:; font-src 'self' data: https:; style-src 'self' 'unsafe-inline' https:; script-src 'self' 'unsafe-inline' 'unsafe-eval' https:; connect-src 'self' https:;"
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=()'
        
        return response

class PermissionMiddleware:
    """
    Middleware para verificar permissões baseado nas URLs.
    Mapeia URLs para permissões necessárias.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Mapeamento de URLs para permissões necessárias
        self.url_permissions = {
            r'^/api/relatorios/': {
                'GET': 'ver_relatorios',
                'POST': 'criar_relatorios',
                'PUT': 'editar_relatorios',
                'DELETE': 'excluir_relatorios'
            },
            r'^/api/faturacao/faturas/': {
                'GET': 'ver_faturas',
                'POST': 'criar_faturas',
                'PUT': 'editar_faturas',
                'DELETE': 'excluir_faturas'
            },
            r'^/api/estoque/produtos/': {
                'GET': 'ver_produtos',
                'POST': 'criar_produtos',
                'PUT': 'editar_produtos',
                'DELETE': 'excluir_produtos'
            },
            # Adicione mais mapeamentos conforme necessário
        }

    def __call__(self, request):
        # Ignora verificação para algumas URLs
        if request.path.startswith('/admin/') or request.path.startswith('/api/auth/'):
            return self.get_response(request)

        # Verifica se é uma requisição para a API
        if request.path.startswith('/api/'):
            # Verifica se o usuário está autenticado
            if not request.user.is_authenticated:
                return JsonResponse(
                    {'error': 'Autenticação necessária'},
                    status=401
                )

            # Superusuários têm acesso total
            if request.user.is_superuser:
                return self.get_response(request)

            # Verifica permissões baseado na URL
            for url_pattern, method_permissions in self.url_permissions.items():
                if re.match(url_pattern, request.path):
                    required_permission = method_permissions.get(request.method)
                    if required_permission:
                        if not request.user.has_perm(required_permission):
                            return JsonResponse(
                                {
                                    'error': 'Permissão negada',
                                    'permissao_necessaria': required_permission
                                },
                                status=403
                            )
                    break

        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Processa a view antes de sua execução para verificar permissões específicas.
        """
        # Verifica se a view tem permissões específicas definidas
        if hasattr(view_func, 'permission_required'):
            if not request.user.is_authenticated:
                return JsonResponse(
                    {'error': 'Autenticação necessária'},
                    status=401
                )

            if not request.user.is_superuser:
                required_permission = getattr(view_func, 'permission_required')
                if isinstance(required_permission, str):
                    required_permission = [required_permission]
                
                for permission in required_permission:
                    if not request.user.has_perm(permission):
                        return JsonResponse(
                            {
                                'error': 'Permissão negada',
                                'permissao_necessaria': permission
                            },
                            status=403
                        )

        return None 

class DataSanitizationMiddleware:
    """
    Middleware para sanitizar dados de entrada e saída.
    Protege contra XSS e injeção de dados maliciosos.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Sanitiza dados de entrada
        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                if request.content_type == 'application/json':
                    # Sanitiza dados JSON
                    body = request.body.decode('utf-8')
                    if body:
                        data = json.loads(body)
                        sanitized_data = self._sanitize_dict(data)
                        request._body = json.dumps(sanitized_data).encode('utf-8')
                else:
                    # Sanitiza dados de formulário
                    request.POST = self._sanitize_dict(request.POST.copy())
            except (json.JSONDecodeError, UnicodeDecodeError):
                return JsonResponse(
                    {'error': 'Dados inválidos'},
                    status=400
                )

        # Sanitiza parâmetros da URL
        request.GET = self._sanitize_dict(request.GET.copy())

        # Processa a resposta
        response = self.get_response(request)

        # Sanitiza dados de saída se for JSON
        if response.get('Content-Type', '').startswith('application/json'):
            try:
                content = json.loads(response.content.decode('utf-8'))
                sanitized_content = self._sanitize_dict(content)
                response.content = json.dumps(sanitized_content, cls=DjangoJSONEncoder).encode('utf-8')
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass

        return response

    def _sanitize_dict(self, data):
        """
        Sanitiza recursivamente todos os valores em um dicionário.
        """
        if isinstance(data, dict):
            return {k: self._sanitize_dict(v) for k, v in data.items()}
        elif isinstance(data, (list, tuple)):
            return [self._sanitize_dict(item) for item in data]
        elif isinstance(data, str):
            return self._sanitize_string(data)
        return data

    def _sanitize_string(self, value):
        """
        Sanitiza uma string para prevenir XSS e outros ataques.
        """
        # Remove caracteres NULL
        value = value.replace('\x00', '')
        
        # Escapa HTML
        value = html.escape(value)
        
        # Remove scripts potencialmente maliciosos
        value = re.sub(r'javascript:', '', value, flags=re.IGNORECASE)
        value = re.sub(r'data:', '', value, flags=re.IGNORECASE)
        value = re.sub(r'vbscript:', '', value, flags=re.IGNORECASE)
        
        # Remove comentários HTML
        value = re.sub(r'<!--.*?-->', '', value)
        
        return value

class SQLInjectionPreventionMiddleware:
    """
    Middleware para prevenir SQL Injection.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Padrões comuns de SQL injection
        self.sql_patterns = [
            r'(\W)*(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER)(\W)+',
            r'--',
            r';',
            r'\/\*.*?\*\/',
            r'xp_.*',
            r'exec\s+.*',
        ]

    def __call__(self, request):
        # Verifica se é uma requisição para a API
        if request.path.startswith('/api/'):
            # Verifica dados POST
            if request.method in ['POST', 'PUT', 'PATCH']:
                try:
                    if request.content_type == 'application/json':
                        body = request.body.decode('utf-8')
                        if body:
                            self._check_sql_injection(body)
                except (json.JSONDecodeError, UnicodeDecodeError):
                    return JsonResponse(
                        {'error': 'Dados inválidos'},
                        status=400
                    )

            # Verifica parâmetros da URL
            for key, value in request.GET.items():
                if isinstance(value, str):
                    self._check_sql_injection(value)

        return self.get_response(request)

    def _check_sql_injection(self, value):
        """
        Verifica se uma string contém padrões suspeitos de SQL injection.
        """
        for pattern in self.sql_patterns:
            if re.search(pattern, value, re.IGNORECASE):
                raise Exception('Possível tentativa de SQL injection detectada')