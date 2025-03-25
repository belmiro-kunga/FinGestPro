from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import PacoteSubscricao, Subscricao
from .serializers import PacoteSubscricaoSerializer, SubscricaoSerializer
from usuarios.permissions import IsSuperAdmin, IsAdminEmpresa

# Create your views here.

class PacoteSubscricaoViewSet(viewsets.ModelViewSet):
    queryset = PacoteSubscricao.objects.all()
    serializer_class = PacoteSubscricaoSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'])
    def ativar_desativar(self, request, pk=None):
        pacote = self.get_object()
        pacote.ativo = not pacote.ativo
        pacote.save()
        return Response({
            'status': 'success',
            'ativo': pacote.ativo
        })

class SubscricaoViewSet(viewsets.ModelViewSet):
    serializer_class = SubscricaoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.tipo == 'super_admin':
            return Subscricao.objects.all()
        elif user.tipo == 'admin_empresa':
            return Subscricao.objects.filter(empresa=user.empresa)
        return Subscricao.objects.none()

    def perform_create(self, serializer):
        # Apenas super_admin pode criar subscrições
        if not self.request.user.tipo == 'super_admin':
            return Response({
                'error': 'Apenas super administradores podem criar subscrições'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer.save()

    @action(detail=True, methods=['post'])
    def renovar(self, request, pk=None):
        # Apenas super_admin ou admin da empresa pode renovar
        subscricao = self.get_object()
        user = request.user
        
        if not (user.tipo == 'super_admin' or 
                (user.tipo == 'admin_empresa' and user.empresa == subscricao.empresa)):
            return Response({
                'error': 'Sem permissão para renovar esta subscrição'
            }, status=status.HTTP_403_FORBIDDEN)

        # Calcula nova data de fim
        if subscricao.periodo == 'mensal':
            nova_data_fim = subscricao.data_fim + timezone.timedelta(days=30)
        else:
            nova_data_fim = subscricao.data_fim + timezone.timedelta(days=365)

        # Atualiza a subscrição
        subscricao.data_fim = nova_data_fim
        subscricao.status = 'ativa'
        subscricao.save()

        return Response({
            'status': 'success',
            'message': 'Subscrição renovada com sucesso',
            'nova_data_fim': nova_data_fim
        })

    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        subscricao = self.get_object()
        user = request.user

        # Verifica permissões
        if not (user.tipo == 'super_admin' or 
                (user.tipo == 'admin_empresa' and user.empresa == subscricao.empresa)):
            return Response({
                'error': 'Sem permissão para cancelar esta subscrição'
            }, status=status.HTTP_403_FORBIDDEN)

        subscricao.status = 'cancelada'
        subscricao.save()

        return Response({
            'status': 'success',
            'message': 'Subscrição cancelada com sucesso'
        })

    @action(detail=True, methods=['get'])
    def status_detalhado(self, request, pk=None):
        subscricao = self.get_object()
        return Response({
            'status': subscricao.status,
            'esta_ativa': subscricao.esta_ativa(),
            'pode_adicionar_usuario': subscricao.pode_adicionar_usuario(),
            'usuarios_ativos': subscricao.usuarios_ativos,
            'max_usuarios': subscricao.pacote.max_usuarios,
            'data_fim': subscricao.data_fim,
            'proxima_fatura': subscricao.proxima_fatura
        })
