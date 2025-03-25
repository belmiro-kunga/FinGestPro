from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from usuarios.models import Empresa
from clientes.models import Clientes

class Quartos(models.Model):
    TIPO_CHOICES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite'),
        ('luxo', 'Luxo'),
        ('familiar', 'Familiar'),
    ]

    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('ocupado', 'Ocupado'),
        ('manutencao', 'Manutenção'),
    ]

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='quartos',
        verbose_name='Empresa'
    )
    numero = models.CharField(
        max_length=10,
        verbose_name='Número do Quarto'
    )
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        verbose_name='Tipo de Quarto'
    )
    preco_por_noite = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Preço por Noite'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='disponivel',
        verbose_name='Status'
    )
    descricao = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descrição'
    )
    capacidade = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Capacidade (pessoas)'
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
        verbose_name = 'Quarto'
        verbose_name_plural = 'Quartos'
        ordering = ['numero']
        unique_together = ['empresa', 'numero']

    def __str__(self):
        return f"Quarto {self.numero} - {self.get_tipo_display()} ({self.empresa.nome})"

    def save(self, *args, **kwargs):
        # Garante que o preço por noite não seja negativo
        if self.preco_por_noite < 0:
            raise ValueError("O preço por noite não pode ser negativo.")
        super().save(*args, **kwargs)

class Mesas(models.Model):
    STATUS_CHOICES = [
        ('disponivel', 'Disponível'),
        ('ocupada', 'Ocupada'),
        ('reservada', 'Reservada'),
    ]

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='mesas',
        verbose_name='Empresa'
    )
    numero = models.CharField(
        max_length=10,
        verbose_name='Número da Mesa'
    )
    capacidade = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Capacidade (pessoas)'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='disponivel',
        verbose_name='Status'
    )
    descricao = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descrição'
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
        verbose_name = 'Mesa'
        verbose_name_plural = 'Mesas'
        ordering = ['numero']
        unique_together = ['empresa', 'numero']

    def __str__(self):
        return f"Mesa {self.numero} - {self.get_status_display()} ({self.empresa.nome})"

class Reservas(models.Model):
    TIPO_CHOICES = [
        ('quarto', 'Quarto'),
        ('mesa', 'Mesa'),
    ]

    STATUS_CHOICES = [
        ('confirmada', 'Confirmada'),
        ('pendente', 'Pendente'),
        ('cancelada', 'Cancelada'),
    ]

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='reservas',
        verbose_name='Empresa'
    )
    cliente = models.ForeignKey(
        Clientes,
        on_delete=models.PROTECT,
        related_name='reservas',
        verbose_name='Cliente'
    )
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        verbose_name='Tipo de Reserva'
    )
    quarto = models.ForeignKey(
        Quartos,
        on_delete=models.PROTECT,
        related_name='reservas',
        null=True,
        blank=True,
        verbose_name='Quarto'
    )
    mesa = models.ForeignKey(
        Mesas,
        on_delete=models.PROTECT,
        related_name='reservas',
        null=True,
        blank=True,
        verbose_name='Mesa'
    )
    data_inicio = models.DateField(
        verbose_name='Data de Início'
    )
    data_fim = models.DateField(
        verbose_name='Data de Término'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente',
        verbose_name='Status'
    )
    observacao = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observação'
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
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['-data_inicio', '-created_at']
        unique_together = [
            ['empresa', 'quarto', 'data_inicio', 'data_fim'],
            ['empresa', 'mesa', 'data_inicio', 'data_fim']
        ]

    def __str__(self):
        tipo_reserva = self.get_tipo_display()
        if self.tipo == 'quarto':
            item = f"Quarto {self.quarto.numero}"
        else:
            item = f"Mesa {self.mesa.numero}"
        return f"{tipo_reserva} - {item} ({self.cliente.nome})"

    def clean(self):
        from django.core.exceptions import ValidationError

        # Validação do tipo de reserva e item reservado
        if self.tipo == 'quarto' and not self.quarto:
            raise ValidationError('Quarto é obrigatório para reservas de quarto.')
        if self.tipo == 'mesa' and not self.mesa:
            raise ValidationError('Mesa é obrigatória para reservas de mesa.')
        if self.tipo == 'quarto' and self.mesa:
            raise ValidationError('Mesa não deve ser informada para reservas de quarto.')
        if self.tipo == 'mesa' and self.quarto:
            raise ValidationError('Quarto não deve ser informado para reservas de mesa.')

        # Validação das datas
        if self.data_fim < self.data_inicio:
            raise ValidationError('Data de término não pode ser anterior à data de início.')

        # Verificar disponibilidade
        if self.tipo == 'quarto':
            reservas_existentes = Reservas.objects.filter(
                empresa=self.empresa,
                quarto=self.quarto,
                status__in=['confirmada', 'pendente'],
                data_inicio__lte=self.data_fim,
                data_fim__gte=self.data_inicio
            ).exclude(pk=self.pk)
        else:
            reservas_existentes = Reservas.objects.filter(
                empresa=self.empresa,
                mesa=self.mesa,
                status__in=['confirmada', 'pendente'],
                data_inicio__lte=self.data_fim,
                data_fim__gte=self.data_inicio
            ).exclude(pk=self.pk)

        if reservas_existentes.exists():
            raise ValidationError('Já existe uma reserva para este período.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

        # Atualiza o status do quarto/mesa
        if self.status == 'confirmada':
            if self.tipo == 'quarto':
                self.quarto.status = 'ocupado'
                self.quarto.save()
            else:
                self.mesa.status = 'ocupada'
                self.mesa.save()
        elif self.status == 'cancelada':
            if self.tipo == 'quarto':
                self.quarto.status = 'disponivel'
                self.quarto.save()
            else:
                self.mesa.status = 'disponivel'
                self.mesa.save() 