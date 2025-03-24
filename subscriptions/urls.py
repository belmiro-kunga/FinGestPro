from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlanosAssinaturaViewSet, EmpresasViewSet

router = DefaultRouter()
router.register(r'planos', PlanosAssinaturaViewSet, basename='plano')
router.register(r'empresas', EmpresasViewSet, basename='empresa')

urlpatterns = [
    path('', include(router.urls)),
] 