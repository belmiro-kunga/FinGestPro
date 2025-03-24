from django.contrib import admin
from .models import Clientes

@admin.register(Clientes)
class ClientesAdmin(admin.ModelAdmin):
    list_display = ['nome', 'empresa', 'nif', 'contato', 'email']
    list_filter = ['empresa']
    search_fields = ['nome', 'nif', 'email', 'contato']
    ordering = ['nome']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['empresa']
