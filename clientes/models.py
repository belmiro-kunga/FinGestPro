from django.db import models
from django.utils import timezone

class Cliente(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    endereco = models.TextField()
    data_cadastro = models.DateTimeField(default=timezone.now)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome']