from django.contrib import admin
from .models import Relatorio, ResumoFolhaPagamento

@admin.register(Relatorio)
class RelatorioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'formato', 'empresa', 'usuario', 'data_geracao')
    list_filter = ('tipo', 'formato', 'empresa', 'data_geracao')
    search_fields = ('nome', 'descricao')
    ordering = ('-data_geracao',)
    readonly_fields = ('data_geracao',)
    raw_id_fields = ('empresa', 'usuario')

@admin.register(ResumoFolhaPagamento)
class ResumoFolhaPagamentoAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'funcionario', 'data_pagamento', 'salario_bruto', 'salario_liquido')
    list_filter = ('empresa', 'data_pagamento')
    search_fields = ('empresa', 'funcionario')
    ordering = ('-data_pagamento',)
    readonly_fields = ('empresa', 'funcionario', 'data_pagamento', 'salario_bruto', 'salario_liquido', 'inss_empresa', 'inss_funcionario', 'irt')
