from rest_framework import serializers
from .models import Clientes, Faturas
from subscriptions.serializers import EmpresasSerializer

class ClientesSerializer(serializers.ModelSerializer):
    empresa = EmpresasSerializer(read_only=True)
    empresa_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Clientes
        fields = [
            'id', 'empresa', 'empresa_id', 'nome', 'nif',
            'endereco', 'contato', 'email', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class FaturasSerializer(serializers.ModelSerializer):
    empresa = EmpresasSerializer(read_only=True)
    empresa_id = serializers.IntegerField(write_only=True)
    cliente = ClientesSerializer(read_only=True)
    cliente_id = serializers.IntegerField(write_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Faturas
        fields = [
            'id', 'empresa', 'empresa_id', 'cliente', 'cliente_id',
            'data_emissao', 'valor_total', 'status', 'status_display',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        # Verifica se o cliente pertence à empresa
        cliente = Clientes.objects.get(pk=data['cliente_id'])
        if cliente.empresa_id != data['empresa_id']:
            raise serializers.ValidationError(
                "O cliente deve pertencer à mesma empresa da fatura."
            )
        return data 