from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from usuarios.models import Empresa

class Conta(models.Model):
    TIPO_CHOICES = [
        ('conta_corrente', 'Conta Corrente'),
        ('poupanca', 'Conta Poupança'),
        ('investimento', 'Conta Investimento'),
        ('cartao_credito', 'Cartão de Crédito'),
        ('outros', 'Outros'),
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name='Empresa')
    nome = models.CharField(max_length=100, verbose_name='Nome da Conta')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name='Tipo de Conta')
    banco = models.CharField(max_length=100, verbose_name='Banco')
    agencia = models.CharField(max_length=10, verbose_name='Agência')
    numero = models.CharField(max_length=20, verbose_name='Número da Conta')
    saldo_inicial = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Saldo Inicial'
    )
    saldo_atual = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Saldo Atual'
    )
    ativa = models.BooleanField(default=True, verbose_name='Conta Ativa')
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')

    class Meta:
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'
        ordering = ['nome']
        unique_together = ['empresa', 'nome']

    def __str__(self):
        return f"{self.nome} - {self.banco}"

    def atualizar_saldo(self, valor, tipo='entrada'):
        """
        Atualiza o saldo da conta
        tipo: 'entrada' ou 'saida'
        """
        if tipo == 'entrada':
            self.saldo_atual += valor
        else:
            self.saldo_atual -= valor
        self.save()
