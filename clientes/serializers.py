from rest_framework import serializers
from .models import Clientes
from assinaturas.serializers import EmpresaSerializer

class ClientesSerializer(serializers.ModelSerializer):
    empresa = EmpresaSerializer(read_only=True)
    empresa_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Clientes
        fields = [
            'id', 'empresa', 'empresa_id', 'nome', 'email', 'telefone',
            'nif', 'endereco', 'observacao', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        empresa_id = data.get('empresa_id')
        nif = data.get('nif')
        
        # Verifica se já existe um cliente com o mesmo NIF para a mesma empresa
        if self.instance is None:  # Criação
            if Clientes.objects.filter(empresa_id=empresa_id, nif=nif).exists():
                raise serializers.ValidationError({
                    'nif': 'Já existe um cliente com este NIF para esta empresa.'
                })
        else:  # Atualização
            if Clientes.objects.filter(
                empresa_id=empresa_id,
                nif=nif
            ).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError({
                    'nif': 'Já existe um cliente com este NIF para esta empresa.'
                })
        
        return data