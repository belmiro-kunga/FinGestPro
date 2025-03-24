from rest_framework import serializers
from .models import Funcionarios, FolhaPagamento, BeneficiosSubsidios, RecibosSalario
from subscriptions.serializers import EmpresasSerializer

class FuncionariosSerializer(serializers.ModelSerializer):
    empresa = EmpresasSerializer(read_only=True)
    empresa_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Funcionarios
        fields = [
            'id', 'empresa', 'empresa_id', 'nome', 'nif', 'cargo',
            'departamento', 'data_admissao', 'tipo_contrato', 'salario_base',
            'banco', 'nib', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class FolhaPagamentoSerializer(serializers.ModelSerializer):
    funcionario = FuncionariosSerializer(read_only=True)
    funcionario_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = FolhaPagamento
        fields = [
            'id', 'funcionario', 'funcionario_id', 'data_pagamento',
            'salario_bruto', 'salario_liquido', 'inss_empresa',
            'inss_funcionario', 'irt', 'horas_extras', 'bonus',
            'comissoes', 'subsidios', 'faltas', 'atrasos',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'salario_liquido', 'inss_empresa', 'inss_funcionario',
            'irt', 'created_at', 'updated_at'
        ]

class BeneficiosSubsidiosSerializer(serializers.ModelSerializer):
    folha_pagamento = FolhaPagamentoSerializer(read_only=True)
    folha_pagamento_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = BeneficiosSubsidios
        fields = [
            'id', 'folha_pagamento', 'folha_pagamento_id',
            'tipo', 'valor', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class RecibosSalarioSerializer(serializers.ModelSerializer):
    folha_pagamento = FolhaPagamentoSerializer(read_only=True)
    folha_pagamento_id = serializers.IntegerField(write_only=True)
    arquivo_pdf_url = serializers.SerializerMethodField()

    class Meta:
        model = RecibosSalario
        fields = [
            'id', 'folha_pagamento', 'folha_pagamento_id',
            'arquivo_pdf', 'arquivo_pdf_url', 'data_envio',
            'email_destinatario', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_arquivo_pdf_url(self, obj):
        if obj.arquivo_pdf:
            return self.context['request'].build_absolute_uri(obj.arquivo_pdf.url)
        return None 