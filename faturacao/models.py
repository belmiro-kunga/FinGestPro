from django.db import models
from django.core.validators import EmailValidator, MinValueValidator
from decimal import Decimal
from usuarios.models import Empresa
from django.core.exceptions import ValidationError

class Clientes(models.Model):
    empresa = models.ForeignKey(
        Empresa,
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
        Empresa,
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

class Produtos(models.Model):
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        verbose_name='Empresa'
    )
    codigo = models.CharField(
        max_length=50,
        verbose_name='Código'
    )
    descricao = models.CharField(
        max_length=255,
        verbose_name='Descrição'
    )
    preco_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Preço Unitário'
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
        ordering = ['descricao']
        unique_together = ['empresa', 'codigo']

    def __str__(self):
        return f"{self.codigo} - {self.descricao}"

class ItensFatura(models.Model):
    fatura = models.ForeignKey(
        Faturas,
        on_delete=models.CASCADE,
        related_name='itens',
        verbose_name='Fatura'
    )
    produto = models.ForeignKey(
        Produtos,
        on_delete=models.PROTECT,  # Protege contra deleção acidental
        verbose_name='Produto'
    )
    quantidade = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Quantidade'
    )
    preco_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Preço Unitário'
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Subtotal',
        editable=False
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
        verbose_name = 'Item da Fatura'
        verbose_name_plural = 'Itens da Fatura'
        ordering = ['id']

    def __str__(self):
        return f"{self.produto.descricao} - {self.quantidade} x {self.preco_unitario}"

    def save(self, *args, **kwargs):
        # Calcula o subtotal
        self.subtotal = self.quantidade * self.preco_unitario
        super().save(*args, **kwargs)
        
        # Atualiza o valor total da fatura
        fatura = self.fatura
        fatura.valor_total = sum(item.subtotal for item in fatura.itens.all())
        fatura.save()

class Proformas(models.Model):
    empresa = models.ForeignKey(
        Empresa,
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
        verbose_name='Valor Total',
        default=Decimal('0.00')
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
        verbose_name = 'Proforma'
        verbose_name_plural = 'Proformas'
        ordering = ['-data_emissao']
        indexes = [
            models.Index(fields=['empresa', 'cliente']),
            models.Index(fields=['data_emissao']),
        ]

    def __str__(self):
        return f"Proforma {self.id} - {self.cliente.nome} ({self.data_emissao})"

    def save(self, *args, **kwargs):
        # Garante que o cliente pertence à mesma empresa da proforma
        if self.cliente.empresa_id != self.empresa_id:
            raise ValueError("O cliente deve pertencer à mesma empresa da proforma.")
        super().save(*args, **kwargs)

    def converter_para_fatura(self):
        """Converte a proforma em uma fatura"""
        fatura = Faturas.objects.create(
            empresa=self.empresa,
            cliente=self.cliente,
            data_emissao=self.data_emissao,
            valor_total=self.valor_total,
            status='PENDENTE'
        )
        
        # Copia os itens da proforma para a fatura
        for item in self.itens.all():
            ItensFatura.objects.create(
                fatura=fatura,
                produto=item.produto,
                quantidade=item.quantidade,
                preco_unitario=item.preco_unitario
            )
        
        return fatura

class ItensProforma(models.Model):
    proforma = models.ForeignKey(
        Proformas,
        on_delete=models.CASCADE,
        related_name='itens',
        verbose_name='Proforma'
    )
    produto = models.ForeignKey(
        Produtos,
        on_delete=models.PROTECT,  # Protege contra deleção acidental
        verbose_name='Produto'
    )
    quantidade = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Quantidade'
    )
    preco_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Preço Unitário'
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Subtotal',
        editable=False
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
        verbose_name = 'Item da Proforma'
        verbose_name_plural = 'Itens da Proforma'
        ordering = ['id']

    def __str__(self):
        return f"{self.produto.descricao} - {self.quantidade} x {self.preco_unitario}"

    def save(self, *args, **kwargs):
        # Calcula o subtotal
        self.subtotal = self.quantidade * self.preco_unitario
        super().save(*args, **kwargs)
        
        # Atualiza o valor total da proforma
        proforma = self.proforma
        proforma.valor_total = sum(item.subtotal for item in proforma.itens.all())
        proforma.save()

    def clean(self):
        # Verifica se o produto pertence à mesma empresa da proforma
        if self.produto.empresa_id != self.proforma.empresa_id:
            raise ValidationError(
                "O produto deve pertencer à mesma empresa da proforma."
            )
