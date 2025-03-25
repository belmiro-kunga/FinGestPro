from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from usuarios.models import Empresa

# Create your models here.

class ResumoFolhaPagamento(models.Model):
    empresa = models.CharField(max_length=255, verbose_name='Empresa')
    funcionario = models.CharField(max_length=255, verbose_name='Funcionário')
    data_pagamento = models.DateField(verbose_name='Data de Pagamento')
    salario_bruto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Salário Bruto'
    )
    salario_liquido = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Salário Líquido'
    )
    inss_empresa = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='INSS Empresa'
    )
    inss_funcionario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='INSS Funcionário'
    )
    irt = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='IRT'
    )

    class Meta:
        managed = False  # Indica que este é um modelo para uma view
        db_table = 'resumo_folha_pagamento'
        verbose_name = 'Resumo da Folha de Pagamento'
        verbose_name_plural = 'Resumos da Folha de Pagamento'
        ordering = ['empresa', 'funcionario', 'data_pagamento']

    def __str__(self):
        return f"{self.empresa} - {self.funcionario} - {self.data_pagamento}"

class Relatorio(models.Model):
    TIPO_CHOICES = [
        ('vendas', 'Vendas'),
        ('financeiro', 'Financeiro'),
        ('estoque', 'Estoque'),
        ('rh', 'Recursos Humanos'),
        ('clientes', 'Clientes'),
        ('fornecedores', 'Fornecedores'),
    ]

    FORMATO_CHOICES = [
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV'),
    ]

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name='Empresa')
    nome = models.CharField(max_length=100, verbose_name='Nome do Relatório')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name='Tipo de Relatório')
    descricao = models.TextField(verbose_name='Descrição')
    formato = models.CharField(max_length=10, choices=FORMATO_CHOICES, verbose_name='Formato')
    parametros = models.JSONField(blank=True, null=True, verbose_name='Parâmetros')
    arquivo = models.FileField(upload_to='relatorios/', blank=True, null=True, verbose_name='Arquivo')
    data_geracao = models.DateTimeField(auto_now_add=True, verbose_name='Data de Geração')
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE, verbose_name='Usuário')

    class Meta:
        verbose_name = 'Relatório'
        verbose_name_plural = 'Relatórios'
        ordering = ['-data_geracao']

    def __str__(self):
        return f"{self.nome} - {self.tipo} ({self.formato})"
