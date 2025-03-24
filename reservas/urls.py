from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuartosViewSet, MesasViewSet, ReservasViewSet

router = DefaultRouter()
router.register(r'quartos', QuartosViewSet)
router.register(r'mesas', MesasViewSet)
router.register(r'reservas', ReservasViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 