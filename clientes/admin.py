from django.contrib import admin
from .models import Clientes

@admin.register(Clientes)
class ClientesAdmin(admin.ModelAdmin):
    list_display = ['nome', 'empresa', 'email', 'telefone', 'nif', 'created_at', 'updated_at']
    list_filter = ['empresa']
    search_fields = ['nome', 'email', 'nif']
    ordering = ['nome']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['empresa']
    list_per_page = 25

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('empresa')

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Se estiver editando um objeto existente
            return self.readonly_fields + ('empresa',)
        return self.readonly_fields 