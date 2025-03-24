from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Clientes
from .serializers import ClientesSerializer

class ClientesViewSet(viewsets.ModelViewSet):
    queryset = Clientes.objects.all()
    serializer_class = ClientesSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['empresa']
    search_fields = ['nome', 'email', 'nif']
    ordering_fields = ['nome', 'created_at']
    ordering = ['nome']

    def get_queryset(self):
        queryset = super().get_queryset()
        empresa_id = self.request.query_params.get('empresa_id', None)
        if empresa_id is not None:
            queryset = queryset.filter(empresa_id=empresa_id)
        return queryset.select_related('empresa')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Se estiver editando um objeto existente
            return self.readonly_fields + ('empresa',)
        return self.readonly_fields 