from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Avg
from .models import Quartos, Mesas, Reservas
from .serializers import QuartosSerializer, MesasSerializer, ReservasSerializer

class QuartosViewSet(viewsets.ModelViewSet):
    queryset = Quartos.objects.all()
    serializer_class = QuartosSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['empresa', 'tipo', 'status']
    search_fields = ['numero', 'descricao']
    ordering_fields = ['numero', 'preco_por_noite', 'capacidade', 'created_at']
    ordering = ['numero']

    def get_queryset(self):
        queryset = Quartos.objects.all()
        empresa_id = self.request.query_params.get('empresa_id', None)
        if empresa_id:
            queryset = queryset.filter(empresa_id=empresa_id)
        return queryset.select_related('empresa')

    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        empresa_id = request.query_params.get('empresa_id', None)
        queryset = self.get_queryset()
        
        if empresa_id:
            queryset = queryset.filter(empresa_id=empresa_id)

        total_quartos = queryset.count()
        quartos_disponiveis = queryset.filter(status='disponivel').count()
        quartos_ocupados = queryset.filter(status='ocupado').count()
        quartos_manutencao = queryset.filter(status='manutencao').count()

        # Média de preço por tipo de quarto
        media_precos = queryset.values('tipo').annotate(
            media_preco=Avg('preco_por_noite')
        )

        return Response({
            'total_quartos': total_quartos,
            'quartos_disponiveis': quartos_disponiveis,
            'quartos_ocupados': quartos_ocupados,
            'quartos_manutencao': quartos_manutencao,
            'media_precos_por_tipo': media_precos,
        })

    @action(detail=True, methods=['post'])
    def alterar_status(self, request, pk=None):
        quarto = self.get_object()
        novo_status = request.data.get('status')

        if not novo_status or novo_status not in dict(Quartos.STATUS_CHOICES):
            return Response(
                {'error': 'Status inválido.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        quarto.status = novo_status
        quarto.save()

        return Response({
            'message': f'Status do quarto alterado para {quarto.get_status_display()}',
            'quarto': QuartosSerializer(quarto).data
        })

class MesasViewSet(viewsets.ModelViewSet):
    queryset = Mesas.objects.all()
    serializer_class = MesasSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['empresa', 'status']
    search_fields = ['numero', 'descricao']
    ordering_fields = ['numero', 'capacidade', 'created_at']
    ordering = ['numero']

    def get_queryset(self):
        queryset = Mesas.objects.all()
        empresa_id = self.request.query_params.get('empresa_id', None)
        if empresa_id:
            queryset = queryset.filter(empresa_id=empresa_id)
        return queryset.select_related('empresa')

    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        empresa_id = request.query_params.get('empresa_id', None)
        queryset = self.get_queryset()
        
        if empresa_id:
            queryset = queryset.filter(empresa_id=empresa_id)

        total_mesas = queryset.count()
        mesas_disponiveis = queryset.filter(status='disponivel').count()
        mesas_ocupadas = queryset.filter(status='ocupada').count()
        mesas_reservadas = queryset.filter(status='reservada').count()

        # Média de capacidade das mesas
        media_capacidade = queryset.aggregate(
            media_capacidade=Avg('capacidade')
        )['media_capacidade'] or 0

        return Response({
            'total_mesas': total_mesas,
            'mesas_disponiveis': mesas_disponiveis,
            'mesas_ocupadas': mesas_ocupadas,
            'mesas_reservadas': mesas_reservadas,
            'media_capacidade': round(media_capacidade, 2),
        })

    @action(detail=True, methods=['post'])
    def alterar_status(self, request, pk=None):
        mesa = self.get_object()
        novo_status = request.data.get('status')

        if not novo_status or novo_status not in dict(Mesas.STATUS_CHOICES):
            return Response(
                {'error': 'Status inválido.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        mesa.status = novo_status
        mesa.save()

        return Response({
            'message': f'Status da mesa alterado para {mesa.get_status_display()}',
            'mesa': MesasSerializer(mesa).data
        })

class ReservasViewSet(viewsets.ModelViewSet):
    queryset = Reservas.objects.all()
    serializer_class = ReservasSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['empresa', 'tipo', 'status', 'cliente']
    search_fields = ['cliente__nome', 'observacao']
    ordering_fields = ['data_inicio', 'data_fim', 'created_at']
    ordering = ['-data_inicio', '-created_at']

    def get_queryset(self):
        queryset = Reservas.objects.all()
        empresa_id = self.request.query_params.get('empresa_id', None)
        if empresa_id:
            queryset = queryset.filter(empresa_id=empresa_id)
        return queryset.select_related(
            'empresa', 'cliente', 'quarto', 'mesa'
        )

    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        empresa_id = request.query_params.get('empresa_id', None)
        queryset = self.get_queryset()
        
        if empresa_id:
            queryset = queryset.filter(empresa_id=empresa_id)

        total_reservas = queryset.count()
        reservas_confirmadas = queryset.filter(status='confirmada').count()
        reservas_pendentes = queryset.filter(status='pendente').count()
        reservas_canceladas = queryset.filter(status='cancelada').count()

        # Estatísticas por tipo
        estatisticas_tipo = queryset.values('tipo').annotate(
            total=Count('id'),
            confirmadas=Count('id', filter=models.Q(status='confirmada')),
            pendentes=Count('id', filter=models.Q(status='pendente')),
            canceladas=Count('id', filter=models.Q(status='cancelada'))
        )

        return Response({
            'total_reservas': total_reservas,
            'reservas_confirmadas': reservas_confirmadas,
            'reservas_pendentes': reservas_pendentes,
            'reservas_canceladas': reservas_canceladas,
            'estatisticas_por_tipo': estatisticas_tipo,
        })

    @action(detail=True, methods=['post'])
    def alterar_status(self, request, pk=None):
        reserva = self.get_object()
        novo_status = request.data.get('status')

        if not novo_status or novo_status not in dict(Reservas.STATUS_CHOICES):
            return Response(
                {'error': 'Status inválido.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        reserva.status = novo_status
        reserva.save()

        return Response({
            'message': f'Status da reserva alterado para {reserva.get_status_display()}',
            'reserva': ReservasSerializer(reserva).data
        })

    @action(detail=False, methods=['get'])
    def disponibilidade(self, request):
        empresa_id = request.query_params.get('empresa_id')
        tipo = request.query_params.get('tipo')
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')

        if not all([empresa_id, tipo, data_inicio, data_fim]):
            return Response(
                {'error': 'Todos os parâmetros são obrigatórios.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Busca itens disponíveis
        if tipo == 'quarto':
            items = Quartos.objects.filter(
                empresa_id=empresa_id,
                status='disponivel'
            )
        else:
            items = Mesas.objects.filter(
                empresa_id=empresa_id,
                status='disponivel'
            )

        # Filtra itens com reservas no período
        reservas = Reservas.objects.filter(
            empresa_id=empresa_id,
            tipo=tipo,
            status__in=['confirmada', 'pendente'],
            data_inicio__lte=data_fim,
            data_fim__gte=data_inicio
        )

        if tipo == 'quarto':
            items_ocupados = reservas.values_list('quarto_id', flat=True)
            items = items.exclude(id__in=items_ocupados)
        else:
            items_ocupados = reservas.values_list('mesa_id', flat=True)
            items = items.exclude(id__in=items_ocupados)

        # Serializa os itens disponíveis
        if tipo == 'quarto':
            serializer = QuartosSerializer(items, many=True)
        else:
            serializer = MesasSerializer(items, many=True)

        return Response({
            'items_disponiveis': serializer.data,
            'total_disponiveis': items.count()
        }) 