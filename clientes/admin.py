from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('nome', 'email', 'telefone')
    ordering = ['nome']
    list_per_page = 25

    def get_queryset(self, request):
        return super().get_queryset(request)