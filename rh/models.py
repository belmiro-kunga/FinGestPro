from django.db import models
from django.core.validators import MinValueValidator, EmailValidator
from decimal import Decimal
from usuarios.models import Empresa
import os

class Funcionarios(models.Model):
    TIPO_CONTRATO_CHOICES = [
        ('Efetivo', 'Efetivo'),
        ('Temporário', 'Temporário'),
        ('Estágio', 'Estágio'),
    ]

    STATUS_CHOICES = [
        ('Ativo', 'Ativo'),
        ('Inativo', 'Inativo'),
    ]

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        verbose_name='Empresa'
    )
    nome = models.CharField(max_length=255, verbose_name='Nome do Funcionário')
    nif = models.CharField(max_length=20, unique=True, verbose_name='NIF')
    cargo = models.CharField(max_length=100, blank=True, null=True, verbose_name='Cargo')
    departamento = models.CharField(max_length=100, blank=True, null=True, verbose_name='Departamento')
    data_admissao = models.DateField(verbose_name='Data de Admissão')
    tipo_contrato = models.CharField(
        max_length=50,
        choices=TIPO_CONTRATO_CHOICES,
        verbose_name='Tipo de Contrato'
    )
    salario_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Salário Base'
    )
    banco = models.CharField(max_length=100, blank=True, null=True, verbose_name='Banco')
    nib = models.CharField(max_length=34, blank=True, null=True, verbose_name='NIB')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Ativo',
        verbose_name='Status'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        ordering = ['nome']
        unique_together = ['empresa', 'nif']

    def __str__(self):
        return f"{self.nome} - {self.cargo} ({self.empresa.nome})"

    def clean(self):
        from django.core.exceptions import ValidationError
        # Validar NIB se banco for fornecido
        if self.banco and not self.nib:
            raise ValidationError('O NIB é obrigatório quando o banco é informado.')

class FolhaPagamento(models.Model):
    funcionario = models.ForeignKey(
        Funcionarios,
        on_delete=models.CASCADE,
        verbose_name='Funcionário'
    )
    data_pagamento = models.DateField(verbose_name='Data de Pagamento')
    salario_bruto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Salário Bruto'
    )
    salario_liquido = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Salário Líquido',
        editable=False
    )
    inss_empresa = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='INSS Empresa (8%)',
        editable=False
    )
    inss_funcionario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='INSS Funcionário (3%)',
        editable=False
    )
    irt = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='IRT',
        editable=False
    )
    horas_extras = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Horas Extras'
    )
    bonus = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Bônus'
    )
    comissoes = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Comissões'
    )
    subsidios = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Subsídios'
    )
    faltas = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Faltas'
    )
    atrasos = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Atrasos'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')

    class Meta:
        verbose_name = 'Folha de Pagamento'
        verbose_name_plural = 'Folhas de Pagamento'
        ordering = ['-data_pagamento', 'funcionario']
        unique_together = ['funcionario', 'data_pagamento']

    def __str__(self):
        return f"Folha de {self.funcionario.nome} - {self.data_pagamento.strftime('%m/%Y')}"

    def calcular_inss(self, valor):
        """Calcula o INSS (8% empresa, 3% funcionário)"""
        inss_empresa = valor * Decimal('0.08')
        inss_funcionario = valor * Decimal('0.03')
        return inss_empresa, inss_funcionario

    def calcular_irt(self, valor):
        """Calcula o IRT com escalões progressivos"""
        if valor <= 70000:
            return Decimal('0')
        elif valor <= 100000:
            return (valor - 70000) * Decimal('0.10')
        elif valor <= 250000:
            return 3000 + (valor - 100000) * Decimal('0.13')
        elif valor <= 500000:
            return 22500 + (valor - 250000) * Decimal('0.15')
        else:
            return 60000 + (valor - 500000) * Decimal('0.17')

    def calcular_descontos_faltas_atrasos(self):
        """Calcula descontos por faltas e atrasos"""
        salario_dia = self.salario_bruto / 30
        desconto_faltas = salario_dia * self.faltas
        desconto_atrasos = (salario_dia / 8) * self.atrasos
        return desconto_faltas + desconto_atrasos

    def save(self, *args, **kwargs):
        # Calcula o salário bruto total
        salario_bruto_total = (
            self.salario_bruto +
            self.horas_extras +
            self.bonus +
            self.comissoes +
            self.subsidios
        )

        # Calcula INSS
        self.inss_empresa, self.inss_funcionario = self.calcular_inss(salario_bruto_total)

        # Calcula descontos por faltas e atrasos
        descontos = self.calcular_descontos_faltas_atrasos()

        # Calcula IRT sobre o valor após INSS e descontos
        base_irt = salario_bruto_total - self.inss_funcionario - descontos
        self.irt = self.calcular_irt(base_irt)

        # Calcula salário líquido
        self.salario_liquido = (
            salario_bruto_total -
            self.inss_funcionario -
            self.irt -
            descontos
        )

        super().save(*args, **kwargs)

class BeneficiosSubsidios(models.Model):
    TIPO_CHOICES = [
        ('Alimentação', 'Alimentação'),
        ('Transporte', 'Transporte'),
        ('Férias', 'Férias'),
        ('13º', '13º Salário'),
        ('Subsídio de Natal', 'Subsídio de Natal'),
        ('Subsídio de Férias', 'Subsídio de Férias'),
        ('Subsídio de Alimentação', 'Subsídio de Alimentação'),
        ('Subsídio de Transporte', 'Subsídio de Transporte'),
        ('Outros', 'Outros'),
    ]

    folha_pagamento = models.ForeignKey(
        FolhaPagamento,
        on_delete=models.CASCADE,
        verbose_name='Folha de Pagamento'
    )
    tipo = models.CharField(
        max_length=50,
        choices=TIPO_CHOICES,
        verbose_name='Tipo de Benefício'
    )
    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Valor'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')

    class Meta:
        verbose_name = 'Benefício/Subsídio'
        verbose_name_plural = 'Benefícios e Subsídios'
        ordering = ['tipo']

    def __str__(self):
        return f"{self.tipo} - {self.valor} ({self.folha_pagamento})"

    def save(self, *args, **kwargs):
        # Atualiza o valor total de subsídios na folha de pagamento
        folha = self.folha_pagamento
        folha.subsidios = BeneficiosSubsidios.objects.filter(
            folha_pagamento=folha
        ).exclude(pk=self.pk).aggregate(
            total=models.Sum('valor')
        )['total'] or Decimal('0')
        
        # Adiciona o valor atual se estiver criando/atualizando
        if self.pk:  # Se estiver atualizando
            old_instance = BeneficiosSubsidios.objects.get(pk=self.pk)
            folha.subsidios -= old_instance.valor
        folha.subsidios += self.valor
        
        # Salva a folha de pagamento para recalcular os totais
        folha.save()
        
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Atualiza o valor total de subsídios na folha de pagamento
        folha = self.folha_pagamento
        folha.subsidios -= self.valor
        folha.save()
        
        super().delete(*args, **kwargs)

class RecibosSalario(models.Model):
    folha_pagamento = models.ForeignKey(
        FolhaPagamento,
        on_delete=models.CASCADE,
        verbose_name='Folha de Pagamento'
    )
    arquivo_pdf = models.FileField(
        upload_to='recibos/%Y/%m/',
        verbose_name='Arquivo PDF',
        null=True,
        blank=True
    )
    data_envio = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data de Envio'
    )
    email_destinatario = models.EmailField(
        max_length=100,
        validators=[EmailValidator()],
        verbose_name='Email do Destinatário'
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
        verbose_name = 'Recibo de Salário'
        verbose_name_plural = 'Recibos de Salário'
        ordering = ['-created_at']
        unique_together = ['folha_pagamento']

    def __str__(self):
        return f"Recibo de {self.folha_pagamento.funcionario.nome} - {self.folha_pagamento.data_pagamento.strftime('%m/%Y')}"

    def delete(self, *args, **kwargs):
        # Remove o arquivo PDF ao deletar o recibo
        if self.arquivo_pdf:
            if os.path.isfile(self.arquivo_pdf.path):
                os.remove(self.arquivo_pdf.path)
        super().delete(*args, **kwargs)
