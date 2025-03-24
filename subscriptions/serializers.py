from rest_framework import serializers
from .models import PlanosAssinatura, Empresas

class PlanosAssinaturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanosAssinatura
        fields = ['id', 'nome', 'preco', 'duracao_dias', 'descricao', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class EmpresasSerializer(serializers.ModelSerializer):
    plano_assinatura = PlanosAssinaturaSerializer(read_only=True)
    plano_assinatura_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Empresas
        fields = [
            'id', 'nome', 'nif', 'endereco', 'contato', 'email', 'logo',
            'plano_assinatura', 'plano_assinatura_id', 'data_inicio_assinatura',
            'data_fim_assinatura', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at'] 