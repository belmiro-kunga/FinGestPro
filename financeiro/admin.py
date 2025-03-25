from django.contrib import admin
from .models import Conta

@admin.register(Conta)
class ContaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'banco', 'agencia', 'numero', 'saldo_atual', 'ativa')
    list_filter = ('tipo', 'ativa', 'empresa')
    search_fields = ('nome', 'banco', 'agencia', 'numero')
    ordering = ('nome',)
    readonly_fields = ('data_criacao', 'data_atualizacao')
