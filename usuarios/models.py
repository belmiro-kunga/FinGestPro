from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Empresa(models.Model):
    nome = models.CharField(max_length=200)
    nif = models.CharField(max_length=20, unique=True)
    endereco = models.TextField()
    telefone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    ativa = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def clean(self):
        # Validação do NIF
        if not self.nif.isdigit() or len(self.nif) != 9:
            raise ValidationError({'nif': _('NIF inválido. Deve conter 9 dígitos.')})

    def pode_adicionar_usuario(self):
        """Verifica se a empresa pode adicionar mais usuários baseado na subscrição"""
        try:
            return self.subscricao.pode_adicionar_usuario()
        except:
            return False

    def get_permissoes_disponiveis(self):
        """Retorna as permissões disponíveis no pacote atual"""
        try:
            return self.subscricao.pacote.permissoes.all()
        except:
            return Permission.objects.none()

class Role(models.Model):
    nome = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Nome'
    )
    descricao = models.TextField(
        verbose_name='Descrição'
    )
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='roles',
        verbose_name='Empresa'
    )
    permissoes = models.ManyToManyField(
        Permission,
        verbose_name='Permissões',
        blank=True
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
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
        ordering = ['nome']
        unique_together = ['empresa', 'nome']

    def __str__(self):
        return f"{self.nome} ({self.empresa.nome})"

class UserActivity(models.Model):
    user = models.ForeignKey(
        'Usuario',
        on_delete=models.CASCADE,
        related_name='activities',
        verbose_name='Usuário'
    )
    action = models.CharField(
        max_length=10,
        verbose_name='Ação'
    )
    path = models.CharField(
        max_length=255,
        verbose_name='Caminho'
    )
    ip_address = models.GenericIPAddressField(
        verbose_name='Endereço IP'
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data/Hora'
    )

    class Meta:
        verbose_name = 'Atividade do Usuário'
        verbose_name_plural = 'Atividades dos Usuários'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.path} ({self.timestamp})"

class Usuario(AbstractUser):
    TIPOS_USUARIO = [
        ('super_admin', 'Super Administrador'),
        ('admin_empresa', 'Administrador da Empresa'),
        ('usuario', 'Usuário')
    ]

    tipo = models.CharField(max_length=20, choices=TIPOS_USUARIO, default='usuario')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True, related_name='usuarios')
    telefone = models.CharField(max_length=20, blank=True)
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
        null=True,
        blank=True
    )
    cargo = models.CharField(max_length=100, blank=True)
    foto = models.ImageField(upload_to='fotos_usuarios/', null=True, blank=True)
    ultimo_login = models.DateTimeField(null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios',
        verbose_name='Perfil'
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

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['username']
        unique_together = ['empresa', 'username', 'email']

    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"

    def save(self, *args, **kwargs):
        # Se for super_admin, não deve ter empresa associada
        if self.tipo == 'super_admin':
            self.empresa = None
            self.role = None
        
        # Se for admin_empresa ou usuario, deve ter empresa associada
        elif self.tipo in ['admin_empresa', 'usuario'] and not self.empresa:
            raise ValidationError(_('Usuários não super admin devem ter uma empresa associada.'))

        # Verifica se a empresa pode adicionar mais usuários
        if self.empresa and not self.pk:  # Novo usuário
            if not self.empresa.pode_adicionar_usuario():
                raise ValidationError(_('Limite de usuários atingido para esta empresa.'))

        # Configura permissões baseadas no tipo de usuário
        self.groups.clear()
        if self.tipo == 'super_admin':
            self.is_superuser = True
            self.is_staff = True
        elif self.tipo == 'admin_empresa':
            self.is_superuser = False
            self.is_staff = True
            # Adiciona todas as permissões disponíveis no pacote
            if self.empresa:
                self.user_permissions.set(self.empresa.get_permissoes_disponiveis())
        else:  # usuario normal
            self.is_superuser = False
            self.is_staff = False
            # Limpa permissões e usa apenas as do Role
            self.user_permissions.clear()
            if self.role:
                # Verifica se as permissões do role estão dentro das permissões do pacote
                permissoes_disponiveis = self.empresa.get_permissoes_disponiveis()
                permissoes_validas = self.role.permissoes.filter(id__in=permissoes_disponiveis)
                self.user_permissions.set(permissoes_validas)

        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.tipo in ['admin_empresa', 'usuario'] and not self.empresa:
            raise ValidationError({'empresa': _('Empresa é obrigatória para este tipo de usuário.')})
        
        # Verifica se as permissões do role estão disponíveis no pacote
        if self.role and self.empresa:
            permissoes_disponiveis = self.empresa.get_permissoes_disponiveis()
            permissoes_invalidas = self.role.permissoes.exclude(id__in=permissoes_disponiveis)
            if permissoes_invalidas.exists():
                raise ValidationError({
                    'role': _('O perfil contém permissões não disponíveis no pacote atual da empresa.')
                })

    def has_perm(self, perm, obj=None):
        # Super admin tem todas as permissões
        if self.tipo == 'super_admin':
            return True
        
        # Verifica se a empresa tem uma subscrição ativa
        if self.empresa and hasattr(self.empresa, 'subscricao'):
            if not self.empresa.subscricao.esta_ativa():
                return False

            # Para admin_empresa, verifica se a permissão está disponível no pacote
            if self.tipo == 'admin_empresa':
                return perm in [p.codename for p in self.empresa.get_permissoes_disponiveis()]
            
            # Para usuário normal, verifica se tem a permissão através do role
            if self.tipo == 'usuario':
                if self.role:
                    return perm in [p.codename for p in self.role.permissoes.all()]
                return False

        return False

    def get_permissoes_disponiveis(self):
        """Retorna as permissões que podem ser atribuídas ao usuário"""
        if self.tipo == 'super_admin':
            return Permission.objects.all()
        elif self.empresa:
            return self.empresa.get_permissoes_disponiveis()
        return Permission.objects.none()

    def save(self, *args, **kwargs):
        # Garante que o email seja único por empresa
        if self.empresa:  # Só verifica se houver empresa
            if not self.pk:  # Se é uma nova instância
                if Usuario.objects.filter(empresa=self.empresa, email=self.email).exists():
                    raise ValueError('Já existe um usuário com este email nesta empresa.')
            else:  # Se é uma atualização
                if Usuario.objects.filter(empresa=self.empresa, email=self.email).exclude(pk=self.pk).exists():
                    raise ValueError('Já existe um usuário com este email nesta empresa.')

        # Atualiza as permissões do usuário baseado no role
        super().save(*args, **kwargs)
        if self.role:
            self.user_permissions.set(self.role.permissoes.all())
        
    def has_module_perms(self, app_label):
        """
        Verifica se o usuário tem permissões para acessar um módulo/app específico.
        Superusuários têm acesso a todos os módulos.
        """
        if self.is_superuser:
            return True
            
        # Verifica permissões do role para o módulo
        if self.role:
            return self.role.permissoes.filter(content_type__app_label=app_label).exists()
            
        return False
