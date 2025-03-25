from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PacoteSubscricaoViewSet, SubscricaoViewSet

router = DefaultRouter()
router.register(r'pacotes', PacoteSubscricaoViewSet)
router.register(r'subscricoes', SubscricaoViewSet, basename='subscricao')

urlpatterns = [
    path('', include(router.urls)),
] 