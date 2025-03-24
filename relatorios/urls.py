from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResumoFolhaPagamentoViewSet

router = DefaultRouter()
router.register('resumo-folha-pagamento', ResumoFolhaPagamentoViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 