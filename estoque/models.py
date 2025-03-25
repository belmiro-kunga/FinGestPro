from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from usuarios.models import Empresa

class EstoqueProdutos(models.Model):
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='estoque_produtos',
        verbose_name='Empresa'
    )
    nome = models.CharField(
        max_length=255,
        verbose_name='Nome do Produto'
    )
    descricao = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descrição'
    )
    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Preço'
    )
    stock = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Estoque'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Criação'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Data de Atualização'
    )

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['nome']
        unique_together = ['empresa', 'nome']

    def __str__(self):
        return f"{self.nome} ({self.empresa.nome})"

    def save(self, *args, **kwargs):
        # Garante que o estoque não seja negativo
        if self.stock < 0:
            raise ValueError("O estoque não pode ser negativo.")
        super().save(*args, **kwargs)

class MovimentacoesEstoque(models.Model):
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ]

    produto = models.ForeignKey(
        EstoqueProdutos,
        on_delete=models.CASCADE,
        related_name='movimentacoes_estoque',
        verbose_name='Produto'
    )
    tipo = models.CharField(
        max_length=10,
        choices=TIPO_CHOICES,
        verbose_name='Tipo de Movimentação'
    )
    quantidade = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Quantidade'
    )
    data = models.DateField(
        verbose_name='Data da Movimentação'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Criação'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Data de Atualização'
    )

    class Meta:
        verbose_name = 'Movimentação de Estoque'
        verbose_name_plural = 'Movimentações de Estoque'
        ordering = ['-data', '-created_at']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.produto.nome} ({self.quantidade})"

    def save(self, *args, **kwargs):
        # Atualiza o estoque do produto
        if self.tipo == 'entrada':
            self.produto.stock += self.quantidade
        else:
            if self.produto.stock < self.quantidade:
                raise ValueError("Estoque insuficiente para realizar a saída.")
            self.produto.stock -= self.quantidade

        # Salva a movimentação
        super().save(*args, **kwargs)
        # Salva o produto com o novo estoque
        self.produto.save()

    def delete(self, *args, **kwargs):
        # Reverte o estoque antes de deletar
        if self.tipo == 'entrada':
            self.produto.stock -= self.quantidade
        else:
            self.produto.stock += self.quantidade
        self.produto.save()
        super().delete(*args, **kwargs)

class Produtos(models.Model):
    nome = models.CharField(max_length=255, verbose_name='Nome')
    stock = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Estoque'
    )

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['nome']

    def __str__(self):
        return self.nome