from rest_framework import serializers
from .models import Clientes, Faturas, Produtos, ItensFatura, Proformas, ItensProforma
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

class ProdutosSerializer(serializers.ModelSerializer):
    empresa = EmpresasSerializer(read_only=True)
    empresa_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Produtos
        fields = [
            'id', 'empresa', 'empresa_id', 'codigo', 'descricao',
            'preco_unitario', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class ItensFaturaSerializer(serializers.ModelSerializer):
    produto = ProdutosSerializer(read_only=True)
    produto_id = serializers.IntegerField(write_only=True)
    fatura = FaturasSerializer(read_only=True)
    fatura_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ItensFatura
        fields = [
            'id', 'fatura', 'fatura_id', 'produto', 'produto_id',
            'quantidade', 'preco_unitario', 'subtotal',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['subtotal', 'created_at', 'updated_at']

    def validate(self, data):
        # Verifica se o produto pertence à mesma empresa da fatura
        produto = Produtos.objects.get(pk=data['produto_id'])
        fatura = Faturas.objects.get(pk=data['fatura_id'])
        
        if produto.empresa_id != fatura.empresa_id:
            raise serializers.ValidationError(
                "O produto deve pertencer à mesma empresa da fatura."
            )
        return data

class ProformasSerializer(serializers.ModelSerializer):
    empresa = EmpresasSerializer(read_only=True)
    empresa_id = serializers.IntegerField(write_only=True)
    cliente = ClientesSerializer(read_only=True)
    cliente_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Proformas
        fields = [
            'id', 'empresa', 'empresa_id', 'cliente', 'cliente_id',
            'data_emissao', 'valor_total', 'created_at', 'updated_at'
        ]
        read_only_fields = ['valor_total', 'created_at', 'updated_at']

    def validate(self, data):
        # Verifica se o cliente pertence à empresa
        cliente = Clientes.objects.get(pk=data['cliente_id'])
        if cliente.empresa_id != data['empresa_id']:
            raise serializers.ValidationError(
                "O cliente deve pertencer à mesma empresa da proforma."
            )
        return data

class ItensProformaSerializer(serializers.ModelSerializer):
    produto = ProdutosSerializer(read_only=True)
    produto_id = serializers.IntegerField(write_only=True)
    proforma = ProformasSerializer(read_only=True)
    proforma_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ItensProforma
        fields = [
            'id', 'proforma', 'proforma_id', 'produto', 'produto_id',
            'quantidade', 'preco_unitario', 'subtotal',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['subtotal', 'created_at', 'updated_at']

    def validate(self, data):
        # Verifica se o produto pertence à mesma empresa da proforma
        produto = Produtos.objects.get(pk=data['produto_id'])
        proforma = Proformas.objects.get(pk=data['proforma_id'])
        
        if produto.empresa_id != proforma.empresa_id:
            raise serializers.ValidationError(
                "O produto deve pertencer à mesma empresa da proforma."
            )
        return data 