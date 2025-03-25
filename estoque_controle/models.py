from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver

class MovimentacoesEstoque(models.Model):
    TIPO_CHOICES = [
        ('Entrada', 'Entrada'),
        ('Saída', 'Saída'),
    ]

    produto = models.ForeignKey(
        'estoque.Produtos',  # Assumindo que existe um modelo Produtos no app estoque
        on_delete=models.PROTECT,
        related_name='movimentacoes',
        verbose_name='Produto'
    )
    tipo = models.CharField(
        max_length=10,
        choices=TIPO_CHOICES,
        verbose_name='Tipo de Movimentação'
    )
    quantidade = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Quantidade'
    )
    data = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data da Movimentação'
    )
    observacao = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observação'
    )

    class Meta:
        verbose_name = 'Movimentação de Estoque'
        verbose_name_plural = 'Movimentações de Estoque'
        ordering = ['-data']

    def __str__(self):
        return f"{self.tipo} - {self.produto.nome} - {self.quantidade}"

    def clean(self):
        if self.tipo == 'Saída' and self.quantidade > self.produto.stock:
            raise ValidationError({
                'quantidade': f'Quantidade insuficiente em estoque. Disponível: {self.produto.stock}'
            })

@receiver(post_save, sender='faturacao.ItensFatura')
def atualizar_estoque(sender, instance, created, **kwargs):
    """
    Signal que atualiza o estoque quando um item é adicionado a uma fatura
    """
    if created:  # Só executa quando um novo item é criado
        # Atualiza o estoque do produto
        produto = instance.produto
        produto.stock -= instance.quantidade
        produto.save()

        # Registra a movimentação
        MovimentacoesEstoque.objects.create(
            produto=produto,
            tipo='Saída',
            quantidade=instance.quantidade,
            observacao=f'Saída automática - Fatura #{instance.fatura.id}'
        )
