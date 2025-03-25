from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class BaseModel(models.Model):
    """Modelo base com campos comuns para todos os outros modelos"""
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    criado_por = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        null=True,
        related_name='%(class)s_criados'
    )
    atualizado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='%(class)s_atualizados'
    )
    ativo = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.criado_em = timezone.now()
        self.atualizado_em = timezone.now()
        return super().save(*args, **kwargs)

class Empresa(BaseModel):
    """Modelo para armazenar informações da empresa"""
    nome = models.CharField(max_length=200)
    razao_social = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=14, unique=True)
    inscricao_estadual = models.CharField(max_length=20, blank=True, null=True)
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    endereco = models.CharField(max_length=200)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=8)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)

    def __str__(self):
        return self.nome

class Configuracao(BaseModel):
    """Modelo para armazenar configurações do sistema"""
    empresa = models.OneToOneField(Empresa, on_delete=models.CASCADE)
    moeda = models.CharField(max_length=3, default='BRL')
    timezone = models.CharField(max_length=50, default='America/Sao_Paulo')
    tema = models.CharField(max_length=50, default='default')
    notificacoes_email = models.BooleanField(default=True)
    backup_automatico = models.BooleanField(default=True)
    intervalo_backup = models.IntegerField(default=24)  # em horas

    def __str__(self):
        return f'Configurações - {self.empresa.nome}'
