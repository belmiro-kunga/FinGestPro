from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Usuario, Empresa, Role, UserActivity

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'tipo', 'empresa', 'cargo', 'role', 'is_active', 'data_criacao')
    list_filter = ('tipo', 'empresa', 'role', 'is_active', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'empresa__nome')
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Informações Pessoais'), {'fields': ('first_name', 'last_name', 'email', 'telefone', 'nif', 'foto')}),
        (_('Informações Profissionais'), {'fields': ('tipo', 'empresa', 'cargo', 'role')}),
        (_('Permissões'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',),
        }),
        (_('Datas Importantes'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'tipo', 'empresa', 'role'),
        }),
    )

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if not request.user.is_superuser:
            # Remove campos que não devem ser visíveis para admin da empresa
            fieldsets = [
                (None, {'fields': ('username', 'password')}),
                (_('Informações Pessoais'), {'fields': ('first_name', 'last_name', 'email', 'telefone', 'nif', 'foto')}),
                (_('Informações Profissionais'), {'fields': ('cargo', 'role')}),
                (_('Status'), {'fields': ('is_active',)}),
            ]
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            # Admin da empresa não pode alterar tipo, empresa ou permissões especiais
            return ('tipo', 'empresa', 'is_superuser', 'is_staff', 'user_permissions', 'groups')
        return super().get_readonly_fields(request, obj)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Admin da empresa só vê usuários da sua empresa
        return qs.filter(empresa=request.user.empresa, tipo='usuario')

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            # Define valores padrão para usuários criados por admin da empresa
            obj.tipo = 'usuario'
            obj.empresa = request.user.empresa
            obj.is_superuser = False
            obj.is_staff = False
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "empresa":
                kwargs["queryset"] = Empresa.objects.filter(id=request.user.empresa.id)
            elif db_field.name == "role":
                kwargs["queryset"] = Role.objects.filter(empresa=request.user.empresa)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            if obj and obj.tipo != 'usuario':
                return False
        return super().has_delete_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            if obj and obj.tipo != 'usuario':
                return False
        return super().has_change_permission(request, obj)

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'nif', 'email', 'ativa', 'data_criacao')
    list_filter = ('ativa',)
    search_fields = ('nome', 'nif', 'email')
    ordering = ('nome',)
    
    fieldsets = (
        (None, {'fields': ('nome', 'nif', 'endereco')}),
        (_('Contato'), {'fields': ('telefone', 'email', 'website')}),
        (_('Configurações'), {'fields': ('logo', 'ativa')}),
    )

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ('nif',)
        return super().get_readonly_fields(request, obj)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(id=request.user.empresa.id)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('nome', 'empresa', 'created_at')
    list_filter = ('empresa',)
    search_fields = ('nome', 'empresa__nome')
    ordering = ('empresa', 'nome')
    
    fieldsets = (
        (None, {'fields': ('nome', 'descricao', 'empresa')}),
        (_('Permissões'), {'fields': ('permissoes',)}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(empresa=request.user.empresa)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "empresa":
                kwargs["queryset"] = Empresa.objects.filter(id=request.user.empresa.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ('empresa',)
        return super().get_readonly_fields(request, obj)

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'path', 'ip_address', 'timestamp')
    list_filter = ('action', 'user__empresa', 'timestamp')
    search_fields = ('user__username', 'path', 'ip_address')
    ordering = ('-timestamp',)
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        return False  # Atividades são criadas automaticamente

    def has_change_permission(self, request, obj=None):
        return False  # Atividades não podem ser alteradas

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # Apenas super admin pode deletar

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.tipo == 'admin_empresa':
            return qs.filter(user__empresa=request.user.empresa)
        return qs.filter(user=request.user)  # Usuários comuns só veem suas próprias atividades
