from django.contrib import admin
from .models import Quartos, Mesas, Reservas

@admin.register(Quartos)
class QuartosAdmin(admin.ModelAdmin):
    list_display = [
        'numero', 'empresa', 'tipo', 'preco_por_noite',
        'status', 'capacidade', 'created_at', 'updated_at'
    ]
    list_filter = ['empresa', 'tipo', 'status']
    search_fields = ['numero', 'descricao']
    ordering = ['numero']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['empresa']
    list_per_page = 25

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('empresa')

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Se estiver editando um objeto existente
            return self.readonly_fields + ('empresa',)
        return self.readonly_fields

@admin.register(Mesas)
class MesasAdmin(admin.ModelAdmin):
    list_display = [
        'numero', 'empresa', 'capacidade', 'status',
        'created_at', 'updated_at'
    ]
    list_filter = ['empresa', 'status']
    search_fields = ['numero', 'descricao']
    ordering = ['numero']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['empresa']
    list_per_page = 25

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('empresa')

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Se estiver editando um objeto existente
            return self.readonly_fields + ('empresa',)
        return self.readonly_fields

@admin.register(Reservas)
class ReservasAdmin(admin.ModelAdmin):
    list_display = [
        'tipo', 'cliente', 'data_inicio', 'data_fim',
        'status', 'created_at', 'updated_at'
    ]
    list_filter = ['empresa', 'tipo', 'status']
    search_fields = ['cliente__nome', 'observacao']
    ordering = ['-data_inicio', '-created_at']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['empresa', 'cliente', 'quarto', 'mesa']
    list_per_page = 25

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'empresa', 'cliente', 'quarto', 'mesa'
        )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Se estiver editando um objeto existente
            return self.readonly_fields + ('empresa', 'cliente', 'tipo', 'quarto', 'mesa')
        return self.readonly_fields 