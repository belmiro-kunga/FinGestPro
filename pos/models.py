from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from decimal import Decimal
from estoque.models import EstoqueProdutos
from usuarios.models import Empresa

class Venda(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_transferencia', 'Em Transferência'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name='Empresa')
    data_venda = models.DateTimeField(auto_now_add=True, verbose_name='Data da Venda')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'),
                              validators=[MinValueValidator(Decimal('0.00'))], verbose_name='Total')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente', verbose_name='Status')
    data_ultima_transferencia = models.DateTimeField(null=True, blank=True, verbose_name='Data da Última Transferência')
    motivo_transferencia = models.TextField(null=True, blank=True, verbose_name='Motivo da Transferência')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                              related_name='vendas_criadas', verbose_name='Usuário Criador')
    usuario_atual = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                    related_name='vendas_atuais', verbose_name='Usuário Atual')

    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'
        ordering = ['-data_venda']
        permissions = [
            ('pode_transferir_venda', 'Pode transferir venda para outro usuário'),
            ('pode_receber_venda', 'Pode receber venda transferida'),
        ]

    def __str__(self):
        return f'Venda #{self.id} - {self.data_venda.strftime("%d/%m/%Y %H:%M")}'

    def calcular_total(self):
        self.total = sum(item.subtotal for item in self.itens.all())
        self.save()

class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='itens', verbose_name='Venda')
    produto = models.ForeignKey(EstoqueProdutos, on_delete=models.PROTECT, verbose_name='Produto')
    quantidade = models.IntegerField(validators=[MinValueValidator(1)], verbose_name='Quantidade')
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2,
                                       validators=[MinValueValidator(Decimal('0.01'))], verbose_name='Preço Unitário')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2,
                                 validators=[MinValueValidator(Decimal('0.01'))], verbose_name='Subtotal')

    class Meta:
        verbose_name = 'Item da Venda'
        verbose_name_plural = 'Itens da Venda'
        ordering = ['id']

    def __str__(self):
        return f'{self.produto.nome} - {self.quantidade}x'

    def save(self, *args, **kwargs):
        self.subtotal = self.quantidade * self.preco_unitario
        super().save(*args, **kwargs)
        self.venda.calcular_total()

class Pagamento(models.Model):
    FORMA_PAGAMENTO_CHOICES = [
        ('dinheiro', 'Dinheiro'),
        ('cartao_credito', 'Cartão de Crédito'),
        ('cartao_debito', 'Cartão de Débito'),
        ('pix', 'PIX'),
        ('transferencia', 'Transferência Bancária'),
    ]

    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='pagamentos', verbose_name='Venda')
    valor = models.DecimalField(max_digits=10, decimal_places=2,
                              validators=[MinValueValidator(Decimal('0.01'))], verbose_name='Valor')
    forma_pagamento = models.CharField(max_length=20, choices=FORMA_PAGAMENTO_CHOICES, verbose_name='Forma de Pagamento')
    data_pagamento = models.DateTimeField(auto_now_add=True, verbose_name='Data do Pagamento')
    observacoes = models.TextField(null=True, blank=True, verbose_name='Observações')

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
        ordering = ['-data_pagamento']

    def __str__(self):
        return f'Pagamento {self.forma_pagamento} - R$ {self.valor:.2f}'
