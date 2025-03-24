from django.contrib import admin
from .models import Clientes, Faturas, Produtos, ItensFatura, Proformas, ItensProforma

@admin.register(Clientes)
class ClientesAdmin(admin.ModelAdmin):
    list_display = ['nome', 'empresa', 'nif', 'contato', 'email']
    list_filter = ['empresa']
    search_fields = ['nome', 'nif', 'email', 'contato']
    ordering = ['nome']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['empresa']

@admin.register(Faturas)
class FaturasAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'empresa', 'cliente', 'data_emissao',
        'valor_total', 'status', 'created_at'
    ]
    list_filter = ['status', 'empresa', 'data_emissao']
    search_fields = ['cliente__nome', 'cliente__nif']
    ordering = ['-data_emissao']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['empresa', 'cliente']
    date_hierarchy = 'data_emissao'

@admin.register(Produtos)
class ProdutosAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'descricao', 'empresa', 'preco_unitario']
    list_filter = ['empresa']
    search_fields = ['codigo', 'descricao']
    ordering = ['descricao']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['empresa']

@admin.register(ItensFatura)
class ItensFaturaAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'fatura', 'produto', 'quantidade',
        'preco_unitario', 'subtotal'
    ]
    list_filter = ['fatura__empresa', 'fatura__data_emissao']
    search_fields = ['produto__codigo', 'produto__descricao']
    ordering = ['id']
    readonly_fields = ['subtotal', 'created_at', 'updated_at']
    raw_id_fields = ['fatura', 'produto']

@admin.register(Proformas)
class ProformasAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'empresa', 'cliente', 'data_emissao',
        'valor_total', 'created_at'
    ]
    list_filter = ['empresa', 'data_emissao']
    search_fields = ['cliente__nome', 'cliente__nif']
    ordering = ['-data_emissao']
    readonly_fields = ['valor_total', 'created_at', 'updated_at']
    raw_id_fields = ['empresa', 'cliente']
    date_hierarchy = 'data_emissao'
    
    actions = ['converter_para_fatura']

    def converter_para_fatura(self, request, queryset):
        for proforma in queryset:
            try:
                fatura = proforma.converter_para_fatura()
                self.message_user(
                    request,
                    f'Proforma {proforma.id} convertida para Fatura {fatura.id}'
                )
            except Exception as e:
                self.message_user(
                    request,
                    f'Erro ao converter Proforma {proforma.id}: {str(e)}',
                    level='ERROR'
                )
    converter_para_fatura.short_description = "Converter proformas selecionadas para faturas"

@admin.register(ItensProforma)
class ItensProformaAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'proforma', 'produto', 'quantidade',
        'preco_unitario', 'subtotal'
    ]
    list_filter = ['proforma__empresa', 'proforma__data_emissao']
    search_fields = ['produto__codigo', 'produto__descricao']
    ordering = ['id']
    readonly_fields = ['subtotal', 'created_at', 'updated_at']
    raw_id_fields = ['proforma', 'produto']
