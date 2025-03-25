from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from subscriptions.models import Empresas

class Usuario(AbstractUser):
    # Campos adicionais
    empresa = models.ForeignKey(
        Empresas,
        on_delete=models.CASCADE,
        related_name='usuarios',
        verbose_name='Empresa',
        null=True,  # Permitir nulo para superusuários
        blank=True  # Permitir em branco para superusuários
    )
    telefone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message='Número de telefone deve estar no formato: "+999999999"'
            )
        ],
        verbose_name='Telefone',
        null=True,  # Permitir nulo para superusuários
        blank=True  # Permitir em branco para superusuários
    )
    nif = models.CharField(
        max_length=11,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{11}$',
                message='NIF deve conter 11 dígitos numéricos'
            )
        ],
        verbose_name='NIF',
        null=True,  # Permitir nulo para superusuários
        blank=True  # Permitir em branco para superusuários
    )
    cargo = models.CharField(
        max_length=100,
        verbose_name='Cargo',
        null=True,  # Permitir nulo para superusuários
        blank=True  # Permitir em branco para superusuários
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Ativo'
    )
    last_login_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name='Último IP de Login'
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
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['username']
        unique_together = ['empresa', 'username', 'email']

    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"

    def save(self, *args, **kwargs):
        # Garante que o email seja único por empresa
        if self.empresa:  # Só verifica se houver empresa
            if not self.pk:  # Se é uma nova instância
                if Usuario.objects.filter(empresa=self.empresa, email=self.email).exists():
                    raise ValueError('Já existe um usuário com este email nesta empresa.')
            else:  # Se é uma atualização
                if Usuario.objects.filter(empresa=self.empresa, email=self.email).exclude(pk=self.pk).exists():
                    raise ValueError('Já existe um usuário com este email nesta empresa.')
        super().save(*args, **kwargs)
