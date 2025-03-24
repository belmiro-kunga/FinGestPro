from django.db import models

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
