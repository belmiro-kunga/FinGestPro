from rest_framework import serializers
from django.contrib.auth.models import Permission
from .models import PacoteSubscricao, Subscricao
from usuarios.models import Empresa

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename']

class PacoteSubscricaoSerializer(serializers.ModelSerializer):
    permissoes = PermissionSerializer(many=True, read_only=True)
    permissoes_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    recursos = serializers.JSONField(source='recursos_incluidos', read_only=True)

    class Meta:
        model = PacoteSubscricao
        fields = [
            'id', 'nome', 'tipo', 'descricao', 'preco_mensal', 'preco_anual',
            'max_usuarios', 'max_armazenamento_gb', 'permissoes', 'permissoes_ids',
            'recursos', 'ativo', 'periodo_teste_dias', 'criado_em', 'atualizado_em'
        ]
        read_only_fields = ['criado_em', 'atualizado_em']

    def create(self, validated_data):
        permissoes_ids = validated_data.pop('permissoes_ids', [])
        pacote = PacoteSubscricao.objects.create(**validated_data)
        
        # Se não foram especificadas permissões, aplica as padrão
        if not permissoes_ids:
            pacote.aplicar_permissoes_padrao()
        else:
            permissoes = Permission.objects.filter(id__in=permissoes_ids)
            pacote.permissoes.set(permissoes)
        
        return pacote

    def update(self, instance, validated_data):
        permissoes_ids = validated_data.pop('permissoes_ids', None)
        
        # Atualiza os campos do pacote
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Se o tipo mudou, atualiza os recursos incluídos
        if 'tipo' in validated_data:
            instance.recursos_incluidos = instance.get_recursos_padrao()
        
        # Atualiza permissões se fornecidas
        if permissoes_ids is not None:
            permissoes = Permission.objects.filter(id__in=permissoes_ids)
            instance.permissoes.set(permissoes)
        
        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Adiciona informações extras úteis
        data['tipo_display'] = instance.get_tipo_display()
        data['total_subscricoes'] = instance.subscricao_set.count()
        return data

class SubscricaoSerializer(serializers.ModelSerializer):
    pacote_nome = serializers.CharField(source='pacote.nome', read_only=True)
    empresa_nome = serializers.CharField(source='empresa.nome', read_only=True)
    dias_restantes = serializers.SerializerMethodField()

    class Meta:
        model = Subscricao
        fields = [
            'id', 'empresa', 'empresa_nome', 'pacote', 'pacote_nome',
            'status', 'periodo', 'data_inicio', 'data_fim',
            'ultima_fatura', 'proxima_fatura', 'preco',
            'usuarios_ativos', 'notas', 'dias_restantes'
        ]
        read_only_fields = ['usuarios_ativos']

    def get_dias_restantes(self, obj):
        from django.utils import timezone
        if obj.data_fim:
            delta = obj.data_fim - timezone.now()
            return max(0, delta.days)
        return 0

    def validate(self, data):
        # Verifica se a empresa já tem uma subscrição ativa
        empresa = data.get('empresa')
        if self.instance is None:  # Criando nova subscrição
            if Subscricao.objects.filter(empresa=empresa, status='ativa').exists():
                raise serializers.ValidationError(
                    "Esta empresa já possui uma subscrição ativa"
                )
        
        return data

    def create(self, validated_data):
        # Define o preço baseado no período escolhido
        pacote = validated_data.get('pacote')
        periodo = validated_data.get('periodo', 'mensal')
        if periodo == 'mensal':
            validated_data['preco'] = pacote.preco_mensal
        else:
            validated_data['preco'] = pacote.preco_anual
        
        return super().create(validated_data) 