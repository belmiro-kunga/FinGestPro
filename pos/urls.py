from django.urls import path
from . import views

app_name = 'pos'

urlpatterns = [
    path('', views.lista_vendas, name='lista_vendas'),
    path('venda/nova/', views.iniciar_venda, name='iniciar_venda'),
    path('venda/<int:venda_id>/', views.detalhes_venda, name='detalhes_venda'),
    path('venda/<int:venda_id>/transferir/', views.transferir_venda, name='transferir_venda'),
    path('venda/<int:venda_id>/aceitar-transferencia/', views.aceitar_transferencia, name='aceitar_transferencia'),
    path('venda/<int:venda_id>/rejeitar-transferencia/', views.rejeitar_transferencia, name='rejeitar_transferencia'),
    path('minhas-transferencias/', views.minhas_transferencias, name='minhas_transferencias'),
]
