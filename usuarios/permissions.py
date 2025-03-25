from functools import wraps
from rest_framework.response import Response
from rest_framework import status, permissions
from django.core.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from django.http import JsonResponse

User = get_user_model()

def requer_permissao(permissao):
    """
    Decorator para verificar se o usuário tem a permissão necessária.
    Pode ser usado em views ou métodos de viewsets.
    
    Exemplo de uso:
    @requer_permissao('ver_relatorios')
    def get(self, request):
        ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(view_instance, request, *args, **kwargs):
            # Verifica se o usuário está autenticado
            if not request.user.is_authenticated:
                return Response(
                    {'error': 'Autenticação necessária'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Superusuários têm todas as permissões
            if request.user.is_superuser:
                return view_func(view_instance, request, *args, **kwargs)

            # Verifica se o usuário tem a permissão necessária
            if not request.user.has_perm(permissao):
                return Response(
                    {'error': 'Permissão negada'},
                    status=status.HTTP_403_FORBIDDEN
                )

            return view_func(view_instance, request, *args, **kwargs)
        return _wrapped_view
    return decorator

def requer_permissoes(permissoes):
    """
    Decorator para verificar se o usuário tem todas as permissões necessárias.
    Aceita uma lista de permissões.
    
    Exemplo de uso:
    @requer_permissoes(['ver_relatorios', 'editar_relatorios'])
    def get(self, request):
        ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(view_instance, request, *args, **kwargs):
            # Verifica se o usuário está autenticado
            if not request.user.is_authenticated:
                return Response(
                    {'error': 'Autenticação necessária'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Superusuários têm todas as permissões
            if request.user.is_superuser:
                return view_func(view_instance, request, *args, **kwargs)

            # Verifica se o usuário tem todas as permissões necessárias
            for permissao in permissoes:
                if not request.user.has_perm(permissao):
                    return Response(
                        {
                            'error': 'Permissão negada',
                            'permissao_faltante': permissao
                        },
                        status=status.HTTP_403_FORBIDDEN
                    )

            return view_func(view_instance, request, *args, **kwargs)
        return _wrapped_view
    return decorator

class PermissaoNecessaria:
    """
    Classe para ser usada como permission_classes em viewsets.
    
    Exemplo de uso:
    permission_classes = [PermissaoNecessaria('ver_relatorios')]
    """
    def __init__(self, permissao):
        self.permissao = permissao

    def has_permission(self, request, view):
        # Superusuários têm todas as permissões
        if request.user.is_superuser:
            return True

        # Verifica se o usuário tem a permissão necessária
        return request.user.has_perm(self.permissao)

class PermissoesNecessarias:
    """
    Classe para ser usada como permission_classes em viewsets.
    Verifica múltiplas permissões.
    
    Exemplo de uso:
    permission_classes = [PermissoesNecessarias(['ver_relatorios', 'editar_relatorios'])]
    """
    def __init__(self, permissoes):
        self.permissoes = permissoes

    def has_permission(self, request, view):
        # Superusuários têm todas as permissões
        if request.user.is_superuser:
            return True

        # Verifica se o usuário tem todas as permissões necessárias
        return all(request.user.has_perm(perm) for perm in self.permissoes)

class IsSuperAdmin(permissions.BasePermission):
    """
    Permite acesso apenas para super administradores.
    """
    def has_permission(self, request, view):
        return request.user and request.user.tipo == 'super_admin'

class IsAdminEmpresa(permissions.BasePermission):
    """
    Permite acesso apenas para administradores de empresa.
    """
    def has_permission(self, request, view):
        return request.user and request.user.tipo == 'admin_empresa'

class IsAdminEmpresaOrSuperAdmin(permissions.BasePermission):
    """
    Permite acesso para super administradores ou administradores de empresa.
    """
    def has_permission(self, request, view):
        return request.user and request.user.tipo in ['super_admin', 'admin_empresa']

class HasSubscriptionPermission(permissions.BasePermission):
    """
    Verifica se o usuário tem permissão baseada na subscrição da empresa.
    """
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        if user.tipo == 'super_admin':
            return True

        if not user.empresa:
            return False

        try:
            subscricao = user.empresa.subscricao
            return subscricao.esta_ativa()
        except:
            return False

def requer_permissao(permissao):
    """
    Decorator para verificar permissões específicas.
    Pode ser usado em views ou métodos de viewsets.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user = request.user

            # Super admin tem todas as permissões
            if user.tipo == 'super_admin':
                return view_func(request, *args, **kwargs)

            # Verifica se o usuário tem a permissão
            if not user.has_perm(permissao):
                return JsonResponse({
                    'error': 'Permissão negada',
                    'permissao_necessaria': permissao
                }, status=403)

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def requer_permissoes(permissoes):
    """
    Decorator para verificar múltiplas permissões.
    Todas as permissões devem ser satisfeitas.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user = request.user

            # Super admin tem todas as permissões
            if user.tipo == 'super_admin':
                return view_func(request, *args, **kwargs)

            # Verifica se o usuário tem todas as permissões
            for permissao in permissoes:
                if not user.has_perm(permissao):
                    return JsonResponse({
                        'error': 'Permissão negada',
                        'permissao_necessaria': permissao
                    }, status=403)

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def requer_tipo_usuario(tipos):
    """
    Decorator para verificar o tipo do usuário.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user = request.user

            if not isinstance(tipos, (list, tuple)):
                tipos_lista = [tipos]
            else:
                tipos_lista = tipos

            if user.tipo not in tipos_lista:
                return JsonResponse({
                    'error': 'Acesso negado',
                    'message': 'Tipo de usuário não autorizado'
                }, status=403)

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator 