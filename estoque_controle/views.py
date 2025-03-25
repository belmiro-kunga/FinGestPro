from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Sum
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import MovimentacoesEstoque
from .serializers import MovimentacoesEstoqueSerializer

# Create your views here.

class MovimentacoesEstoqueViewSet(viewsets.ModelViewSet):
    queryset = MovimentacoesEstoque.objects.all()
    serializer_class = MovimentacoesEstoqueSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['produto', 'tipo']
    search_fields = ['produto__nome', 'observacao']
    ordering_fields = ['data', 'produto__nome', 'quantidade']
    ordering = ['-data']

    def get_queryset(self):
        queryset = super().get_queryset()
        data_inicio = self.request.query_params.get('data_inicio', None)
        data_fim = self.request.query_params.get('data_fim', None)

        if data_inicio:
            queryset = queryset.filter(data__date__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data__date__lte=data_fim)

        return queryset.select_related('produto')

    @action(detail=False, methods=['get'])
    def resumo(self, request):
        """
        Retorna um resumo das movimentações agrupadas por produto
        """
        queryset = self.get_queryset()
        resumo = []

        # Agrupa as movimentações por produto
        produtos = queryset.values('produto', 'produto__nome').distinct()
        
        for produto in produtos:
            movs = queryset.filter(produto=produto['produto'])
            entradas = movs.filter(tipo='Entrada').aggregate(
                total=Sum('quantidade')
            )['total'] or 0
            saidas = movs.filter(tipo='Saída').aggregate(
                total=Sum('quantidade')
            )['total'] or 0

            resumo.append({
                'produto': produto['produto__nome'],
                'entradas': entradas,
                'saidas': saidas,
                'saldo': entradas - saidas
            })

        return Response(resumo)
