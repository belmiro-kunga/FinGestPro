from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from usuarios.models import Empresa

class Fornecedor(models.Model):
    TIPO_CHOICES = [
        ('empresa', 'Empresa'),
        ('individual', 'Individual'),
        ('associacao', 'Associação'),
        ('cooperativa', 'Cooperativa'),
        ('outros', 'Outros'),
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name='Empresa')
    nome = models.CharField(max_length=200, verbose_name='Nome/Razão Social')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name='Tipo de Fornecedor')
    nif = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='NIF',
        help_text='Número de Identificação Fiscal'
    )
    email = models.EmailField(verbose_name='E-mail')
    telefone = models.CharField(
        max_length=20,
        verbose_name='Telefone',
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message='Número de telefone deve ser inserido no formato: "+999999999"'
        )]
    )
    endereco = models.TextField(verbose_name='Endereço')
    cidade = models.CharField(max_length=100, verbose_name='Cidade')
    estado = models.CharField(max_length=2, verbose_name='Estado')
    cep = models.CharField(
        max_length=8,
        verbose_name='CEP',
        validators=[RegexValidator(
            regex=r'^\d{8}$',
            message='CEP deve conter 8 dígitos'
        )]
    )
    website = models.URLField(blank=True, null=True, verbose_name='Website')
    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações')
    ativo = models.BooleanField(default=True, verbose_name='Fornecedor Ativo')
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')

    class Meta:
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'
        ordering = ['nome']
        unique_together = ['empresa', 'nif']

    def __str__(self):
        return f"{self.nome} ({self.nif})"

    def clean(self):
        # Validação do NIF
        if not self.nif.isdigit() or len(self.nif) != 9:
            raise ValidationError({'nif': _('NIF inválido. Deve conter 9 dígitos.')})
