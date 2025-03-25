from rest_framework import serializers
from .models import MovimentacoesEstoque
from estoque.serializers import ProdutosSerializer

class MovimentacoesEstoqueSerializer(serializers.ModelSerializer):
    produto = ProdutosSerializer(read_only=True)
    produto_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MovimentacoesEstoque
        fields = [
            'id', 'produto', 'produto_id', 'tipo', 'quantidade',
            'data', 'observacao'
        ]
        read_only_fields = ['data']

    def validate(self, data):
        # Valida se há estoque suficiente para saídas
        if data.get('tipo') == 'Saída':
            produto = data.get('produto_id')
            quantidade = data.get('quantidade')
            if quantidade > produto.stock:
                raise serializers.ValidationError({
                    'quantidade': f'Quantidade insuficiente em estoque. Disponível: {produto.stock}'
                })
        return data 