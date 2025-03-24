from django.db import models
from django.core.validators import EmailValidator, MinValueValidator
from decimal import Decimal
from subscriptions.models import Empresas

class Clientes(models.Model):
    empresa = models.ForeignKey(
        Empresas,
        on_delete=models.CASCADE,
        verbose_name='Empresa'
    )
    nome = models.CharField(
        max_length=255,
        verbose_name='Nome do Cliente'
    )
    nif = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='NIF'
    )
    endereco = models.TextField(
        blank=True,
        null=True,
        verbose_name='Endereço'
    )
    contato = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Contato'
    )
    email = models.EmailField(
        max_length=100,
        blank=True,
        null=True,
        validators=[EmailValidator()],
        verbose_name='Email'
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
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome']
        unique_together = ['empresa', 'nif']

    def __str__(self):
        return f"{self.nome} ({self.empresa.nome})"

class Faturas(models.Model):
    STATUS_CHOICES = [
        ('PAGA', 'Paga'),
        ('PENDENTE', 'Pendente'),
        ('CANCELADA', 'Cancelada'),
    ]

    empresa = models.ForeignKey(
        Empresas,
        on_delete=models.CASCADE,
        verbose_name='Empresa'
    )
    cliente = models.ForeignKey(
        Clientes,
        on_delete=models.PROTECT,  # Protege contra deleção acidental
        verbose_name='Cliente'
    )
    data_emissao = models.DateField(
        verbose_name='Data de Emissão'
    )
    valor_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Valor Total'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDENTE',
        verbose_name='Status'
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
        verbose_name = 'Fatura'
        verbose_name_plural = 'Faturas'
        ordering = ['-data_emissao']
        indexes = [
            models.Index(fields=['empresa', 'cliente', 'status']),
            models.Index(fields=['data_emissao']),
        ]

    def __str__(self):
        return f"Fatura {self.id} - {self.cliente.nome} ({self.data_emissao})"

    def save(self, *args, **kwargs):
        # Garante que o cliente pertence à mesma empresa da fatura
        if self.cliente.empresa_id != self.empresa_id:
            raise ValueError("O cliente deve pertencer à mesma empresa da fatura.")
        super().save(*args, **kwargs)
