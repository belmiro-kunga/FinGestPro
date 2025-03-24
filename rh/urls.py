from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FuncionariosViewSet, FolhaPagamentoViewSet,
    BeneficiosSubsidiosViewSet, RecibosSalarioViewSet
)

router = DefaultRouter()
router.register(r'funcionarios', FuncionariosViewSet, basename='funcionario')
router.register(r'folha-pagamento', FolhaPagamentoViewSet, basename='folha-pagamento')
router.register(r'beneficios-subsidios', BeneficiosSubsidiosViewSet)
router.register(r'recibos-salario', RecibosSalarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 