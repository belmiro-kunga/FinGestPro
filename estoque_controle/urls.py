from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovimentacoesEstoqueViewSet

router = DefaultRouter()
router.register('movimentacoes', MovimentacoesEstoqueViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 