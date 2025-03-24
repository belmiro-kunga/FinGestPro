from django.db import models
from django.utils import timezone

# Create your models here.

class PlanosAssinatura(models.Model):
    nome = models.CharField(max_length=50, verbose_name='Nome do Plano')
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço')
    duracao_dias = models.IntegerField(verbose_name='Duração em Dias')
    descricao = models.TextField(blank=True, null=True, verbose_name='Descrição')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')

    class Meta:
        verbose_name = 'Plano de Assinatura'
        verbose_name_plural = 'Planos de Assinatura'
        ordering = ['preco']

    def __str__(self):
        return f"{self.nome} - {self.duracao_dias} dias"

class Empresas(models.Model):
    STATUS_CHOICES = [
        ('Ativo', 'Ativo'),
        ('Inativo', 'Inativo'),
        ('Suspenso', 'Suspenso'),
    ]

    nome = models.CharField(max_length=255, verbose_name='Nome da Empresa')
    nif = models.CharField(max_length=20, unique=True, verbose_name='NIF')
    endereco = models.TextField(blank=True, null=True, verbose_name='Endereço')
    contato = models.CharField(max_length=50, blank=True, null=True, verbose_name='Contato')
    email = models.EmailField(max_length=100, blank=True, null=True, verbose_name='E-mail')
    logo = models.CharField(max_length=255, blank=True, null=True, verbose_name='Caminho do Logo')
    plano_assinatura = models.ForeignKey(
        PlanosAssinatura,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Plano de Assinatura'
    )
    data_inicio_assinatura = models.DateField(null=True, blank=True, verbose_name='Data de Início da Assinatura')
    data_fim_assinatura = models.DateField(null=True, blank=True, verbose_name='Data de Fim da Assinatura')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Ativo',
        verbose_name='Status'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.nif}"

    def save(self, *args, **kwargs):
        # Se a empresa estiver ativa e tiver um plano, atualiza as datas de assinatura
        if self.status == 'Ativo' and self.plano_assinatura:
            if not self.data_inicio_assinatura:
                self.data_inicio_assinatura = timezone.now().date()
            if not self.data_fim_assinatura:
                self.data_fim_assinatura = self.data_inicio_assinatura + timezone.timedelta(days=self.plano_assinatura.duracao_dias)
        super().save(*args, **kwargs)
