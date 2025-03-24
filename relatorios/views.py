from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Sum
from .models import ResumoFolhaPagamento
from .serializers import ResumoFolhaPagamentoSerializer
from rest_framework.response import Response

# Create your views here.

class ResumoFolhaPagamentoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ResumoFolhaPagamento.objects.all()
    serializer_class = ResumoFolhaPagamentoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['empresa', 'funcionario']
    search_fields = ['empresa', 'funcionario']
    ordering_fields = ['empresa', 'funcionario', 'data_pagamento']
    ordering = ['-data_pagamento']

    def get_queryset(self):
        queryset = super().get_queryset()
        empresa_id = self.request.query_params.get('empresa_id', None)
        data_inicio = self.request.query_params.get('data_inicio', None)
        data_fim = self.request.query_params.get('data_fim', None)

        if empresa_id:
            queryset = queryset.filter(empresa_id=empresa_id)
        if data_inicio:
            queryset = queryset.filter(data_pagamento__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data_pagamento__lte=data_fim)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        # Calcula totais
        totais = queryset.aggregate(
            total_salario_bruto=Sum('salario_bruto'),
            total_salario_liquido=Sum('salario_liquido'),
            total_inss_empresa=Sum('inss_empresa'),
            total_inss_funcionario=Sum('inss_funcionario'),
            total_irt=Sum('irt')
        )

        return Response({
            'dados': serializer.data,
            'totais': totais
        })
