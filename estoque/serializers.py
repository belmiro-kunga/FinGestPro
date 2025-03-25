from rest_framework import serializers
from .models import EstoqueProdutos, MovimentacoesEstoque, Produtos
from assinaturas.serializers import EmpresaSerializer

class EstoqueProdutosSerializer(serializers.ModelSerializer):
    empresa = EmpresaSerializer(read_only=True)
    empresa_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = EstoqueProdutos
        fields = [
            'id', 'empresa', 'empresa_id', 'nome', 'descricao',
            'preco', 'stock', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        # Verifica se o nome do produto já existe para a mesma empresa
        empresa_id = data.get('empresa_id')
        nome = data.get('nome')
        instance = getattr(self, 'instance', None)

        if instance:
            # Atualização
            exists = EstoqueProdutos.objects.filter(
                empresa_id=empresa_id,
                nome=nome
            ).exclude(pk=instance.pk).exists()
        else:
            # Criação
            exists = EstoqueProdutos.objects.filter(
                empresa_id=empresa_id,
                nome=nome
            ).exists()

        if exists:
            raise serializers.ValidationError(
                "Já existe um produto com este nome para esta empresa."
            )
        return data

class MovimentacoesEstoqueSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)
    
    class Meta:
        model = MovimentacoesEstoque
        fields = [
            'id', 'produto', 'produto_nome', 'tipo', 'quantidade',
            'data', 'observacao', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        """
        Validação personalizada para garantir que:
        1. O produto pertence à empresa do usuário
        2. A quantidade é positiva
        3. Para saídas, há quantidade suficiente em estoque
        """
        request = self.context.get('request')
        produto = data.get('produto')
        quantidade = data.get('quantidade')
        tipo = data.get('tipo')

        if produto and produto.empresa != request.user.empresa:
            raise serializers.ValidationError(
                {'produto': 'Produto não pertence à sua empresa'}
            )

        if quantidade <= 0:
            raise serializers.ValidationError(
                {'quantidade': 'A quantidade deve ser maior que zero'}
            )

        if tipo == 'saida' and produto.quantidade < quantidade:
            raise serializers.ValidationError(
                {'quantidade': 'Quantidade insuficiente em estoque'}
            )

        return data

class ProdutosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produtos
        fields = ['id', 'nome', 'stock']
