from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.auth.password_validation import validate_password
from assinaturas.serializers import EmpresaSerializer
from .models import Role

User = get_user_model()

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename']

class RoleSerializer(serializers.ModelSerializer):
    empresa = EmpresaSerializer(read_only=True)
    empresa_id = serializers.IntegerField(write_only=True)
    permissoes = PermissionSerializer(many=True, read_only=True)
    permissoes_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Role
        fields = [
            'id', 'nome', 'descricao', 'empresa', 'empresa_id',
            'permissoes', 'permissoes_ids', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        permissoes_ids = validated_data.pop('permissoes_ids', [])
        role = Role.objects.create(**validated_data)
        if permissoes_ids:
            role.permissoes.set(Permission.objects.filter(id__in=permissoes_ids))
        return role

    def update(self, instance, validated_data):
        permissoes_ids = validated_data.pop('permissoes_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if permissoes_ids is not None:
            instance.permissoes.set(Permission.objects.filter(id__in=permissoes_ids))
        return instance

class UsuarioSerializer(serializers.ModelSerializer):
    empresa = EmpresaSerializer(read_only=True)
    empresa_id = serializers.IntegerField(write_only=True)
    role = RoleSerializer(read_only=True)
    role_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'password2', 'email', 'first_name',
            'last_name', 'empresa', 'empresa_id', 'telefone', 'nif', 'cargo',
            'role', 'role_id', 'is_active', 'last_login_ip', 'created_at', 'updated_at'
        ]
        read_only_fields = ['last_login_ip', 'created_at', 'updated_at']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "As senhas não conferem"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        role_id = validated_data.pop('role_id', None)
        user = User.objects.create_user(**validated_data)
        if role_id:
            user.role_id = role_id
            user.save()
        return user

class UsuarioUpdateSerializer(serializers.ModelSerializer):
    empresa = EmpresaSerializer(read_only=True)
    empresa_id = serializers.IntegerField(write_only=True)
    role = RoleSerializer(read_only=True)
    role_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'empresa', 'empresa_id', 'telefone', 'nif', 'cargo',
            'role', 'role_id', 'is_active', 'last_login_ip', 'created_at', 'updated_at'
        ]
        read_only_fields = ['last_login_ip', 'created_at', 'updated_at']

    def update(self, instance, validated_data):
        role_id = validated_data.pop('role_id', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if role_id is not None:
            instance.role_id = role_id
        instance.save()
        return instance

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "As senhas não conferem"})
        return attrs 