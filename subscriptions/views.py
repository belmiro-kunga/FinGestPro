from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import PlanosAssinatura, Empresas
from .serializers import PlanosAssinaturaSerializer, EmpresasSerializer

# Create your views here.

class PlanosAssinaturaViewSet(viewsets.ModelViewSet):
    queryset = PlanosAssinatura.objects.all()
    serializer_class = PlanosAssinaturaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

class EmpresasViewSet(viewsets.ModelViewSet):
    queryset = Empresas.objects.all()
    serializer_class = EmpresasSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        queryset = Empresas.objects.all()
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        return queryset
