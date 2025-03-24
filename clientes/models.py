from django.db import models
from subscriptions.models import Empresas

class Clientes(models.Model):
    empresa = models.ForeignKey(
        Empresas,
        on_delete=models.CASCADE,
        related_name='clientes_gerais',
        verbose_name='Empresa'
    )
    nome = models.CharField(
        max_length=100,
        verbose_name='Nome'
    )
    email = models.EmailField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='E-mail'
    )
    telefone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Telefone'
    )
    nif = models.CharField(
        max_length=14,
        blank=True,
        null=True,
        verbose_name='NIF'
    )
    endereco = models.TextField(
        blank=True,
        null=True,
        verbose_name='Endereço'
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
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome']
        unique_together = ['empresa', 'nif']

    def __str__(self):
        return f"{self.nome} ({self.empresa.nome})" 