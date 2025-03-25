from django.contrib import admin
from .models import Venda, ItemVenda

class ItemVendaInline(admin.TabularInline):
    model = ItemVenda
    extra = 1

@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_cliente', 'get_data', 'get_valor_total')
    search_fields = ('cliente__nome',)
    inlines = [ItemVendaInline]

    def get_cliente(self, obj):
        return obj.cliente.nome if obj.cliente else '-'
    get_cliente.short_description = 'Cliente'

    def get_data(self, obj):
        return obj.data_venda.strftime('%d/%m/%Y %H:%M') if obj.data_venda else '-'
    get_data.short_description = 'Data da Venda'

    def get_valor_total(self, obj):
        return f'R$ {obj.valor_total:.2f}' if obj.valor_total else '-'
    get_valor_total.short_description = 'Valor Total'

@admin.register(ItemVenda)
class ItemVendaAdmin(admin.ModelAdmin):
    list_display = ('venda', 'produto', 'quantidade', 'get_valor_unitario')
    search_fields = ('produto__nome',)

    def get_valor_unitario(self, obj):
        return f'R$ {obj.valor_unitario:.2f}' if obj.valor_unitario else '-'
    get_valor_unitario.short_description = 'Valor Unitário'
