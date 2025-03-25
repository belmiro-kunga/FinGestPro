from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import PacoteSubscricao, Subscricao

@admin.register(PacoteSubscricao)
class PacoteSubscricaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'preco_mensal', 'preco_anual', 'max_usuarios', 'ativo')
    list_filter = ('tipo', 'ativo')
    search_fields = ('nome', 'descricao')
    ordering = ('tipo', 'preco_mensal')
    
    fieldsets = (
        (None, {
            'fields': ('nome', 'tipo', 'descricao', 'ativo')
        }),
        (_('Preços'), {
            'fields': ('preco_mensal', 'preco_anual')
        }),
        (_('Limites'), {
            'fields': ('max_usuarios', 'max_armazenamento_gb', 'periodo_teste_dias')
        }),
        (_('Recursos'), {
            'fields': ('permissoes', 'recursos_incluidos')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ('tipo', 'preco_mensal', 'preco_anual', 'max_usuarios', 'max_armazenamento_gb', 'permissoes')
        return super().get_readonly_fields(request, obj)

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

@admin.register(Subscricao)
class SubscricaoAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'pacote', 'status', 'periodo', 'data_inicio', 'data_fim', 'usuarios_ativos')
    list_filter = ('status', 'periodo', 'pacote')
    search_fields = ('empresa__nome', 'pacote__nome')
    ordering = ('-data_inicio',)
    
    fieldsets = (
        (None, {
            'fields': ('empresa', 'pacote', 'status', 'periodo')
        }),
        (_('Datas'), {
            'fields': ('data_inicio', 'data_fim', 'ultima_fatura', 'proxima_fatura')
        }),
        (_('Financeiro'), {
            'fields': ('preco',)
        }),
        (_('Detalhes'), {
            'fields': ('usuarios_ativos', 'notas')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ('empresa', 'pacote', 'preco', 'data_inicio', 'data_fim', 'ultima_fatura', 'proxima_fatura')
        return super().get_readonly_fields(request, obj)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(empresa=request.user.empresa)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "empresa":
                kwargs["queryset"] = request.user.empresa
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
