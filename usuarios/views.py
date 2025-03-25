from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.models import Permission
from django.utils import timezone
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from .serializers import (
    UsuarioSerializer,
    UsuarioUpdateSerializer,
    ChangePasswordSerializer,
    RoleSerializer,
    PermissionSerializer
)
from .models import Role
import jwt
from datetime import datetime, timedelta

User = get_user_model()

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Usuários só podem ver roles da mesma empresa
        return Role.objects.filter(empresa=self.request.user.empresa)

    @action(detail=False, methods=['get'])
    def available_permissions(self, request):
        """Lista todas as permissões disponíveis no sistema"""
        # Obtém todas as permissões do sistema
        content_types = ContentType.objects.all()
        permissions = Permission.objects.filter(content_type__in=content_types)
        serializer = PermissionSerializer(permissions, many=True)
        
        # Agrupa permissões por app
        grouped_permissions = {}
        for perm in serializer.data:
            app_label = perm['codename'].split('_')[0]
            if app_label not in grouped_permissions:
                grouped_permissions[app_label] = []
            grouped_permissions[app_label].append(perm)
            
        return Response(grouped_permissions)

    def perform_create(self, serializer):
        serializer.save(empresa=self.request.user.empresa)

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer

    def get_permissions(self):
        if self.action == 'login':
            return []
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return UsuarioUpdateSerializer
        return UsuarioSerializer

    def get_queryset(self):
        # Usuários só podem ver outros usuários da mesma empresa
        if not self.request.user.is_authenticated:
            return User.objects.none()
        return User.objects.filter(empresa=self.request.user.empresa)

    def perform_create(self, serializer):
        # Registra o IP do usuário
        serializer.save(
            last_login_ip=self.request.META.get('REMOTE_ADDR')
        )

    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        Endpoint para login de usuários.
        Retorna um token JWT se as credenciais estiverem corretas.
        """
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': 'Por favor, forneça username e password'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {'error': 'Credenciais inválidas'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            return Response(
                {'error': 'Usuário está desativado'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Faz login no Django
        login(request, user)

        # Atualiza o último IP de login
        user.last_login_ip = request.META.get('REMOTE_ADDR')
        user.save()

        # Gera tokens JWT
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        # Adiciona claims personalizados ao token
        access_token['username'] = user.username
        access_token['email'] = user.email
        if hasattr(user, 'empresa') and user.empresa:
            access_token['empresa_id'] = user.empresa.id
            access_token['empresa_nome'] = user.empresa.nome
        if hasattr(user, 'role') and user.role:
            access_token['role'] = {
                'id': user.role.id,
                'nome': user.role.nome,
                'permissoes': [p.codename for p in user.role.permissoes.all()]
            }

        response_data = {
            'refresh': str(refresh),
            'access': str(access_token),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'empresa': user.empresa.nome if hasattr(user, 'empresa') and user.empresa else None,
                'cargo': user.cargo if hasattr(user, 'cargo') else None,
                'role': {
                    'id': user.role.id,
                    'nome': user.role.nome,
                    'permissoes': [p.codename for p in user.role.permissoes.all()]
                } if hasattr(user, 'role') and user.role else None,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser
            }
        }

        # Define o URL de redirecionamento baseado no tipo de usuário
        if user.is_superuser:
            response_data['redirect_url'] = '/admin/'
        else:
            response_data['redirect_url'] = '/dashboard/'

        return Response(response_data)

    @action(detail=False, methods=['post'])
    def refresh_token(self, request):
        """Atualiza o token de acesso usando o refresh token"""
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {'error': 'Refresh token é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            refresh = RefreshToken(refresh_token)
            access_token = refresh.access_token

            # Adiciona claims personalizados ao novo token
            user = User.objects.get(id=refresh['user_id'])
            access_token['username'] = user.username
            access_token['email'] = user.email
            if hasattr(user, 'empresa') and user.empresa:
                access_token['empresa_id'] = user.empresa.id
                access_token['empresa_nome'] = user.empresa.nome
            if hasattr(user, 'role') and user.role:
                access_token['role'] = {
                    'id': user.role.id,
                    'nome': user.role.nome,
                    'permissoes': [p.codename for p in user.role.permissoes.all()]
                }

            return Response({
                'access': str(access_token)
            })
        except Exception as e:
            return Response(
                {'error': 'Token inválido ou expirado'},
                status=status.HTTP_401_UNAUTHORIZED
            )

    @action(detail=False, methods=['post'])
    def logout(self, request):
        """Invalida o refresh token atual"""
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logout realizado com sucesso'})
        except Exception:
            return Response(
                {'error': 'Token inválido'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Retorna os dados do usuário atual"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """Altera a senha do usuário atual"""
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.data.get('old_password')):
                return Response(
                    {'old_password': 'Senha incorreta'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response({'message': 'Senha alterada com sucesso'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
