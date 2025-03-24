from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, F
from django.utils import timezone
from .models import EstoqueProdutos, MovimentacoesEstoque
from .serializers import EstoqueProdutosSerializer, MovimentacoesEstoqueSerializer

class EstoqueProdutosViewSet(viewsets.ModelViewSet):
    queryset = EstoqueProdutos.objects.all()
    serializer_class = EstoqueProdutosSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['empresa']
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome', 'preco', 'stock', 'created_at']
    ordering = ['nome']

    def get_queryset(self):
        queryset = EstoqueProdutos.objects.all()
        empresa_id = self.request.query_params.get('empresa_id', None)
        if empresa_id:
            queryset = queryset.filter(empresa_id=empresa_id)
        return queryset

    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        empresa_id = request.query_params.get('empresa_id', None)
        queryset = self.get_queryset()
        
        if empresa_id:
            queryset = queryset.filter(empresa_id=empresa_id)

        total_produtos = queryset.count()
        valor_total_estoque = sum(
            produto.stock * produto.preco for produto in queryset
        )
        produtos_baixo_estoque = queryset.filter(stock__lte=10).count()
        produtos_sem_estoque = queryset.filter(stock=0).count()

        return Response({
            'total_produtos': total_produtos,
            'valor_total_estoque': valor_total_estoque,
            'produtos_baixo_estoque': produtos_baixo_estoque,
            'produtos_sem_estoque': produtos_sem_estoque,
        })

    @action(detail=True, methods=['post'])
    def ajustar_estoque(self, request, pk=None):
        produto = self.get_object()
        quantidade = request.data.get('quantidade')
        tipo = request.data.get('tipo')  # 'entrada' ou 'saida'

        if not quantidade or not tipo:
            return Response(
                {'error': 'Quantidade e tipo são obrigatórios.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            quantidade = int(quantidade)
            if quantidade <= 0:
                raise ValueError("A quantidade deve ser maior que zero.")
        except ValueError:
            return Response(
                {'error': 'Quantidade inválida.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if tipo == 'saida' and produto.stock < quantidade:
            return Response(
                {'error': 'Estoque insuficiente.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if tipo == 'entrada':
            produto.stock += quantidade
        else:
            produto.stock -= quantidade

        produto.save()

        return Response({
            'message': f'Estoque ajustado com sucesso. Novo estoque: {produto.stock}',
            'produto': EstoqueProdutosSerializer(produto).data
        })

class MovimentacoesEstoqueViewSet(viewsets.ModelViewSet):
    serializer_class = MovimentacoesEstoqueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MovimentacoesEstoque.objects.filter(
            produto__empresa=self.request.user.empresa
        ).select_related('produto')

    def perform_create(self, serializer):
        produto = serializer.validated_data['produto']
        quantidade = serializer.validated_data['quantidade']
        tipo = serializer.validated_data['tipo']

        # Atualiza o estoque do produto
        if tipo == 'entrada':
            produto.quantidade = F('quantidade') + quantidade
        else:  # saída
            if produto.quantidade < quantidade:
                raise serializers.ValidationError(
                    {'quantidade': 'Quantidade insuficiente em estoque'}
                )
            produto.quantidade = F('quantidade') - quantidade

        produto.save()
        serializer.save()

    def perform_update(self, serializer):
        raise serializers.ValidationError(
            {'detail': 'Movimentações de estoque não podem ser alteradas'}
        )

    @action(detail=False, methods=['get'])
    def relatorio(self, request):
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')
        produto_id = request.query_params.get('produto_id')

        queryset = self.get_queryset()

        if data_inicio:
            queryset = queryset.filter(data__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data__lte=data_fim)
        if produto_id:
            queryset = queryset.filter(produto_id=produto_id)

        # Agrupa por produto e calcula totais
        relatorio = queryset.values('produto__nome').annotate(
            total_entradas=Sum(
                F('quantidade') * (F('tipo') == 'entrada')
            ),
            total_saidas=Sum(
                F('quantidade') * (F('tipo') == 'saida')
            )
        )

        return Response(relatorio)
