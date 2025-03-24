from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from django.utils import timezone
from .models import Clientes, Faturas
from .serializers import ClientesSerializer, FaturasSerializer

# Create your views here.

class ClientesViewSet(viewsets.ModelViewSet):
    queryset = Clientes.objects.all()
    serializer_class = ClientesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['empresa']
    search_fields = ['nome', 'nif', 'email', 'contato']
    ordering_fields = ['nome', 'created_at']
    ordering = ['nome']

    def get_queryset(self):
        queryset = Clientes.objects.all()
        empresa_id = self.request.query_params.get('empresa_id', None)
        if empresa_id:
            queryset = queryset.filter(empresa_id=empresa_id)
        return queryset

class FaturasViewSet(viewsets.ModelViewSet):
    queryset = Faturas.objects.all()
    serializer_class = FaturasSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['empresa', 'cliente', 'status']
    search_fields = ['cliente__nome', 'status']
    ordering_fields = ['data_emissao', 'valor_total', 'created_at']
    ordering = ['-data_emissao']

    def get_queryset(self):
        queryset = Faturas.objects.all()
        empresa_id = self.request.query_params.get('empresa_id', None)
        cliente_id = self.request.query_params.get('cliente_id', None)
        status = self.request.query_params.get('status', None)
        data_inicio = self.request.query_params.get('data_inicio', None)
        data_fim = self.request.query_params.get('data_fim', None)

        if empresa_id:
            queryset = queryset.filter(empresa_id=empresa_id)
        if cliente_id:
            queryset = queryset.filter(cliente_id=cliente_id)
        if status:
            queryset = queryset.filter(status=status.upper())
        if data_inicio:
            queryset = queryset.filter(data_emissao__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data_emissao__lte=data_fim)

        return queryset

    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        empresa_id = request.query_params.get('empresa_id', None)
        data_inicio = request.query_params.get('data_inicio', None)
        data_fim = request.query_params.get('data_fim', None)

        queryset = self.get_queryset()
        if empresa_id:
            queryset = queryset.filter(empresa_id=empresa_id)
        if data_inicio:
            queryset = queryset.filter(data_emissao__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data_emissao__lte=data_fim)

        total_faturas = queryset.count()
        valor_total = queryset.aggregate(total=Sum('valor_total'))['total'] or 0
        faturas_pagas = queryset.filter(status='PAGA').count()
        valor_pago = queryset.filter(status='PAGA').aggregate(
            total=Sum('valor_total'))['total'] or 0
        faturas_pendentes = queryset.filter(status='PENDENTE').count()
        valor_pendente = queryset.filter(status='PENDENTE').aggregate(
            total=Sum('valor_total'))['total'] or 0

        return Response({
            'total_faturas': total_faturas,
            'valor_total': valor_total,
            'faturas_pagas': faturas_pagas,
            'valor_pago': valor_pago,
            'faturas_pendentes': faturas_pendentes,
            'valor_pendente': valor_pendente,
        })
