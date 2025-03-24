from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EstoqueProdutosViewSet, MovimentacoesEstoqueViewSet

router = DefaultRouter()
router.register(r'produtos', EstoqueProdutosViewSet)
router.register(r'movimentacoes', MovimentacoesEstoqueViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
