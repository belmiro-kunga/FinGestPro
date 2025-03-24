from rest_framework import serializers
from .models import ResumoFolhaPagamento

class ResumoFolhaPagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumoFolhaPagamento
        fields = [
            'empresa', 'funcionario', 'data_pagamento', 'salario_bruto',
            'salario_liquido', 'inss_empresa', 'inss_funcionario', 'irt'
        ] 