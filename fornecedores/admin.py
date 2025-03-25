from django.contrib import admin
from .models import Fornecedor

@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'nif', 'email', 'telefone', 'cidade', 'ativo')
    list_filter = ('tipo', 'ativo', 'empresa')
    search_fields = ('nome', 'nif', 'email', 'telefone', 'cidade')
    ordering = ('nome',)
    readonly_fields = ('data_cadastro', 'data_atualizacao')
