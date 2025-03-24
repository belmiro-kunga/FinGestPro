from django.contrib import admin
from .models import PlanosAssinatura, Empresas

@admin.register(PlanosAssinatura)
class PlanosAssinaturaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'duracao_dias', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('nome', 'descricao')
    ordering = ('preco',)

@admin.register(Empresas)
class EmpresasAdmin(admin.ModelAdmin):
    list_display = ('nome', 'nif', 'status', 'plano_assinatura', 'data_inicio_assinatura', 'data_fim_assinatura')
    list_filter = ('status', 'plano_assinatura', 'created_at', 'updated_at')
    search_fields = ('nome', 'nif', 'email', 'contato')
    ordering = ('nome',)
    readonly_fields = ('created_at', 'updated_at')
