from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from subscriptions.serializers import EmpresasSerializer

User = get_user_model()

class UsuarioSerializer(serializers.ModelSerializer):
    empresa = EmpresasSerializer(read_only=True)
    empresa_id = serializers.IntegerField(write_only=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'password2', 'email', 'first_name',
            'last_name', 'empresa', 'empresa_id', 'telefone', 'nif', 'cargo',
            'is_active', 'last_login_ip', 'created_at', 'updated_at'
        ]
        read_only_fields = ['last_login_ip', 'created_at', 'updated_at']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "As senhas não conferem"})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class UsuarioUpdateSerializer(serializers.ModelSerializer):
    empresa = EmpresasSerializer(read_only=True)
    empresa_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'empresa', 'empresa_id', 'telefone', 'nif', 'cargo',
            'is_active', 'last_login_ip', 'created_at', 'updated_at'
        ]
        read_only_fields = ['last_login_ip', 'created_at', 'updated_at']

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "As senhas não conferem"})
        return attrs 