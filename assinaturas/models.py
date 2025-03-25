from django.db import models
from django.contrib.auth.models import Permission
from django.utils import timezone

class PacoteSubscricao(models.Model):
    TIPO_CHOICES = [
        ('basico', 'Básico'),
        ('profissional', 'Profissional'),
        ('enterprise', 'Enterprise')
    ]

    nome = models.CharField(max_length=100, unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='basico')
    descricao = models.TextField()
    preco_mensal = models.DecimalField(max_digits=10, decimal_places=2)
    preco_anual = models.DecimalField(max_digits=10, decimal_places=2)
    max_usuarios = models.IntegerField(default=5)
    max_armazenamento_gb = models.IntegerField(default=5)
    permissoes = models.ManyToManyField(Permission, related_name='pacotes')
    recursos_incluidos = models.JSONField(default=dict)  # Armazena recursos específicos do pacote
    ativo = models.BooleanField(default=True)
    periodo_teste_dias = models.IntegerField(default=15)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Pacote de Subscrição'
        verbose_name_plural = 'Pacotes de Subscrição'
        ordering = ['preco_mensal']

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"

    def save(self, *args, **kwargs):
        # Define recursos padrão baseado no tipo
        if not self.recursos_incluidos:
            self.recursos_incluidos = self.get_recursos_padrao()
        super().save(*args, **kwargs)

    def get_recursos_padrao(self):
        """
        Define os recursos padrão baseado no tipo do pacote
        """
        recursos_base = {
            'relatorios_basicos': True,
            'suporte_email': True,
            'backup_diario': True,
        }

        if self.tipo == 'basico':
            return {
                **recursos_base,
                'max_faturas_mes': 100,
                'relatorios_avancados': False,
                'suporte_prioritario': False,
                'api_access': False,
                'white_label': False,
            }
        elif self.tipo == 'profissional':
            return {
                **recursos_base,
                'max_faturas_mes': 1000,
                'relatorios_avancados': True,
                'suporte_prioritario': True,
                'api_access': True,
                'white_label': False,
            }
        else:  # enterprise
            return {
                **recursos_base,
                'max_faturas_mes': -1,  # ilimitado
                'relatorios_avancados': True,
                'suporte_prioritario': True,
                'api_access': True,
                'white_label': True,
            }

    def get_permissoes_padrao(self):
        """
        Retorna as permissões padrão baseado no tipo do pacote
        """
        permissoes_base = [
            'view_fatura',
            'add_fatura',
            'view_produto',
            'add_produto',
            'view_cliente',
            'add_cliente',
        ]

        if self.tipo == 'basico':
            return permissoes_base
        
        permissoes_pro = permissoes_base + [
            'change_fatura',
            'delete_fatura',
            'change_produto',
            'delete_produto',
            'change_cliente',
            'delete_cliente',
            'view_relatorio_avancado',
        ]

        if self.tipo == 'profissional':
            return permissoes_pro

        # Enterprise tem todas as permissões
        return permissoes_pro + [
            'view_api',
            'manage_white_label',
            'export_data',
            'import_data',
        ]

    def aplicar_permissoes_padrao(self):
        """
        Aplica as permissões padrão ao pacote
        """
        permissoes = Permission.objects.filter(codename__in=self.get_permissoes_padrao())
        self.permissoes.set(permissoes)

    def tem_recurso(self, recurso):
        """
        Verifica se o pacote tem um recurso específico
        """
        return self.recursos_incluidos.get(recurso, False)

    def dentro_limite_usuarios(self, num_usuarios):
        """
        Verifica se está dentro do limite de usuários
        """
        return num_usuarios <= self.max_usuarios

    def dentro_limite_armazenamento(self, tamanho_gb):
        """
        Verifica se está dentro do limite de armazenamento
        """
        return tamanho_gb <= self.max_armazenamento_gb

class Subscricao(models.Model):
    STATUS_CHOICES = [
        ('ativa', 'Ativa'),
        ('pendente', 'Pendente'),
        ('cancelada', 'Cancelada'),
        ('expirada', 'Expirada')
    ]

    PERIODO_CHOICES = [
        ('mensal', 'Mensal'),
        ('anual', 'Anual')
    ]

    empresa = models.OneToOneField('usuarios.Empresa', on_delete=models.CASCADE, related_name='subscricao')
    pacote = models.ForeignKey(PacoteSubscricao, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    periodo = models.CharField(max_length=10, choices=PERIODO_CHOICES, default='mensal')
    data_inicio = models.DateTimeField(default=timezone.now)
    data_fim = models.DateTimeField()
    ultima_fatura = models.DateTimeField(null=True, blank=True)
    proxima_fatura = models.DateTimeField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    usuarios_ativos = models.IntegerField(default=0)
    notas = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Subscrição'
        verbose_name_plural = 'Subscrições'
        ordering = ['-data_inicio']

    def __str__(self):
        return f"{self.empresa.nome} - {self.pacote.nome}"

    def save(self, *args, **kwargs):
        # Define a data de fim baseada no período
        if not self.data_fim:
            if self.periodo == 'mensal':
                self.data_fim = self.data_inicio + timezone.timedelta(days=30)
            else:
                self.data_fim = self.data_inicio + timezone.timedelta(days=365)
        
        # Define a próxima fatura
        if not self.proxima_fatura:
            if self.periodo == 'mensal':
                self.proxima_fatura = self.data_inicio + timezone.timedelta(days=30)
            else:
                self.proxima_fatura = self.data_inicio + timezone.timedelta(days=365)

        # Define o preço baseado no período
        if not self.preco:
            if self.periodo == 'mensal':
                self.preco = self.pacote.preco_mensal
            else:
                self.preco = self.pacote.preco_anual

        super().save(*args, **kwargs)

    def esta_ativa(self):
        return (
            self.status == 'ativa' and 
            self.data_fim > timezone.now() and 
            self.usuarios_ativos <= self.pacote.max_usuarios
        )

    def pode_adicionar_usuario(self):
        return self.usuarios_ativos < self.pacote.max_usuarios

    def atualizar_status(self):
        agora = timezone.now()
        if self.data_fim < agora:
            self.status = 'expirada'
        elif self.status == 'pendente' and self.data_inicio <= agora:
            self.status = 'ativa'
        self.save()
