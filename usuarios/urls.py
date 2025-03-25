from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenBlacklistView
from .views import UsuarioViewSet

router = DefaultRouter()
router.register('usuarios', UsuarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', UsuarioViewSet.as_view({'post': 'login'}), name='login'),
    path('refresh/', UsuarioViewSet.as_view({'post': 'refresh_token'}), name='token_refresh'),
    path('logout/', UsuarioViewSet.as_view({'post': 'logout'}), name='logout'),
    path('me/', UsuarioViewSet.as_view({'get': 'me'}), name='me'),
    path('change-password/', UsuarioViewSet.as_view({'post': 'change_password'}), name='change-password'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
] 