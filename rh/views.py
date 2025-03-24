from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Funcionarios, FolhaPagamento, BeneficiosSubsidios, RecibosSalario
from .serializers import (
    FuncionariosSerializer, FolhaPagamentoSerializer,
    BeneficiosSubsidiosSerializer, RecibosSalarioSerializer
)
from django.utils import timezone

# Create your views here.

class FuncionariosViewSet(viewsets.ModelViewSet):
    queryset = Funcionarios.objects.all()
    serializer_class = FuncionariosSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['empresa', 'status', 'tipo_contrato', 'departamento']
    search_fields = ['nome', 'nif', 'cargo']
    ordering_fields = ['nome', 'data_admissao', 'salario_base']
    ordering = ['nome']

    def get_queryset(self):
        queryset = Funcionarios.objects.all()
        empresa_id = self.request.query_params.get('empresa_id', None)
        if empresa_id:
            queryset = queryset.filter(empresa_id=empresa_id)
        return queryset

class FolhaPagamentoViewSet(viewsets.ModelViewSet):
    queryset = FolhaPagamento.objects.all()
    serializer_class = FolhaPagamentoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['funcionario', 'data_pagamento']
    search_fields = ['funcionario__nome', 'funcionario__nif']
    ordering_fields = ['data_pagamento', 'funcionario__nome', 'salario_liquido']
    ordering = ['-data_pagamento']

    def get_queryset(self):
        queryset = FolhaPagamento.objects.all()
        funcionario_id = self.request.query_params.get('funcionario_id', None)
        data_inicio = self.request.query_params.get('data_inicio', None)
        data_fim = self.request.query_params.get('data_fim', None)

        if funcionario_id:
            queryset = queryset.filter(funcionario_id=funcionario_id)
        if data_inicio:
            queryset = queryset.filter(data_pagamento__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data_pagamento__lte=data_fim)

        return queryset

class BeneficiosSubsidiosViewSet(viewsets.ModelViewSet):
    queryset = BeneficiosSubsidios.objects.all()
    serializer_class = BeneficiosSubsidiosSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['folha_pagamento', 'tipo']
    search_fields = ['tipo', 'folha_pagamento__funcionario__nome']
    ordering_fields = ['tipo', 'valor', 'created_at']
    ordering = ['tipo']

    def get_queryset(self):
        queryset = BeneficiosSubsidios.objects.all()
        folha_id = self.request.query_params.get('folha_id', None)
        tipo = self.request.query_params.get('tipo', None)

        if folha_id:
            queryset = queryset.filter(folha_pagamento_id=folha_id)
        if tipo:
            queryset = queryset.filter(tipo=tipo)

        return queryset

class RecibosSalarioViewSet(viewsets.ModelViewSet):
    queryset = RecibosSalario.objects.all()
    serializer_class = RecibosSalarioSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['folha_pagamento', 'data_envio']
    search_fields = ['email_destinatario', 'folha_pagamento__funcionario__nome']
    ordering_fields = ['data_envio', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = RecibosSalario.objects.all()
        folha_id = self.request.query_params.get('folha_id', None)
        data_inicio = self.request.query_params.get('data_inicio', None)
        data_fim = self.request.query_params.get('data_fim', None)

        if folha_id:
            queryset = queryset.filter(folha_pagamento_id=folha_id)
        if data_inicio:
            queryset = queryset.filter(data_envio__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data_envio__lte=data_fim)

        return queryset

    @action(detail=True, methods=['post'])
    def enviar_email(self, request, pk=None):
        recibo = self.get_object()
        # Aqui você implementaria a lógica de envio de email
        # Por exemplo, usando django.core.mail
        recibo.data_envio = timezone.now()
        recibo.save()
        return Response({'status': 'email enviado'})
