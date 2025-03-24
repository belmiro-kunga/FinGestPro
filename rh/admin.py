from django.contrib import admin
from .models import Funcionarios, FolhaPagamento, BeneficiosSubsidios, RecibosSalario

@admin.register(Funcionarios)
class FuncionariosAdmin(admin.ModelAdmin):
    list_display = ('nome', 'empresa', 'cargo', 'departamento', 'tipo_contrato', 'status', 'data_admissao')
    list_filter = ('empresa', 'status', 'tipo_contrato', 'departamento', 'data_admissao')
    search_fields = ('nome', 'nif', 'cargo')
    ordering = ('nome',)
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('empresa',)

@admin.register(FolhaPagamento)
class FolhaPagamentoAdmin(admin.ModelAdmin):
    list_display = (
        'funcionario', 'data_pagamento', 'salario_bruto',
        'salario_liquido', 'inss_empresa', 'inss_funcionario',
        'irt', 'horas_extras', 'bonus', 'comissoes'
    )
    list_filter = ('funcionario__empresa', 'data_pagamento')
    search_fields = ('funcionario__nome', 'funcionario__nif')
    ordering = ('-data_pagamento', 'funcionario__nome')
    readonly_fields = (
        'salario_liquido', 'inss_empresa', 'inss_funcionario',
        'irt', 'created_at', 'updated_at'
    )
    raw_id_fields = ('funcionario',)

@admin.register(BeneficiosSubsidios)
class BeneficiosSubsidiosAdmin(admin.ModelAdmin):
    list_display = ['folha_pagamento', 'tipo', 'valor', 'created_at']
    list_filter = ['tipo', 'folha_pagamento__funcionario__empresa']
    search_fields = ['tipo', 'folha_pagamento__funcionario__nome']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['folha_pagamento']

@admin.register(RecibosSalario)
class RecibosSalarioAdmin(admin.ModelAdmin):
    list_display = [
        'folha_pagamento', 'email_destinatario',
        'data_envio', 'created_at'
    ]
    list_filter = [
        'data_envio', 'folha_pagamento__funcionario__empresa'
    ]
    search_fields = [
        'email_destinatario',
        'folha_pagamento__funcionario__nome'
    ]
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['folha_pagamento']
