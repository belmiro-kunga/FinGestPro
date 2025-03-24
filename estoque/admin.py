from django.contrib import admin
from .models import EstoqueProdutos, MovimentacoesEstoque

@admin.register(EstoqueProdutos)
class EstoqueProdutosAdmin(admin.ModelAdmin):
    list_display = [
        'nome', 'empresa', 'preco', 'stock',
        'created_at', 'updated_at'
    ]
    list_filter = ['empresa']
    search_fields = ['nome', 'descricao']
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

@admin.register(MovimentacoesEstoque)
class MovimentacoesEstoqueAdmin(admin.ModelAdmin):
    list_display = [
        'produto', 'tipo', 'quantidade', 'data',
        'created_at', 'updated_at'
    ]
    list_filter = ['produto__empresa', 'tipo', 'data']
    search_fields = ['produto__nome']
    ordering = ['-data', '-created_at']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['produto']
    date_hierarchy = 'data'
    list_per_page = 25

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'produto', 'produto__empresa'
        )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Se estiver editando um objeto existente
            return self.readonly_fields + ('produto', 'tipo', 'quantidade')
        return self.readonly_fields
