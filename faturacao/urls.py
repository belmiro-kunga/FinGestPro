from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ClientesViewSet, FaturasViewSet,
    ProdutosViewSet, ItensFaturaViewSet,
    ProformasViewSet, ItensProformaViewSet
)

router = DefaultRouter()
router.register(r'clientes', ClientesViewSet)
router.register(r'faturas', FaturasViewSet)
router.register(r'produtos', ProdutosViewSet)
router.register(r'itens-fatura', ItensFaturaViewSet)
router.register(r'proformas', ProformasViewSet)
router.register(r'itens-proforma', ItensProformaViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 