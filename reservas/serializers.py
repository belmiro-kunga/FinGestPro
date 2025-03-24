from rest_framework import serializers
from .models import Quartos, Mesas, Reservas
from subscriptions.serializers import EmpresasSerializer
from clientes.serializers import ClientesSerializer

class QuartosSerializer(serializers.ModelSerializer):
    empresa = EmpresasSerializer(read_only=True)
    empresa_id = serializers.IntegerField(write_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Quartos
        fields = [
            'id', 'empresa', 'empresa_id', 'numero', 'tipo', 'tipo_display',
            'preco_por_noite', 'status', 'status_display', 'descricao',
            'capacidade', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        # Verifica se o número do quarto já existe para a mesma empresa
        empresa_id = data.get('empresa_id')
        numero = data.get('numero')
        instance = getattr(self, 'instance', None)

        if instance:
            # Atualização
            exists = Quartos.objects.filter(
                empresa_id=empresa_id,
                numero=numero
            ).exclude(pk=instance.pk).exists()
        else:
            # Criação
            exists = Quartos.objects.filter(
                empresa_id=empresa_id,
                numero=numero
            ).exists()

        if exists:
            raise serializers.ValidationError(
                "Já existe um quarto com este número para esta empresa."
            )

        # Validação da capacidade baseada no tipo de quarto
        tipo = data.get('tipo')
        capacidade = data.get('capacidade')
        
        if tipo == 'single' and capacidade > 1:
            raise serializers.ValidationError(
                {'capacidade': 'Quarto single não pode ter capacidade maior que 1 pessoa.'}
            )
        elif tipo == 'double' and capacidade > 2:
            raise serializers.ValidationError(
                {'capacidade': 'Quarto double não pode ter capacidade maior que 2 pessoas.'}
            )

        return data 

class MesasSerializer(serializers.ModelSerializer):
    empresa = EmpresasSerializer(read_only=True)
    empresa_id = serializers.IntegerField(write_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Mesas
        fields = [
            'id', 'empresa', 'empresa_id', 'numero', 'capacidade',
            'status', 'status_display', 'descricao', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        # Verifica se o número da mesa já existe para a mesma empresa
        empresa_id = data.get('empresa_id')
        numero = data.get('numero')
        instance = getattr(self, 'instance', None)

        if instance:
            # Atualização
            exists = Mesas.objects.filter(
                empresa_id=empresa_id,
                numero=numero
            ).exclude(pk=instance.pk).exists()
        else:
            # Criação
            exists = Mesas.objects.filter(
                empresa_id=empresa_id,
                numero=numero
            ).exists()

        if exists:
            raise serializers.ValidationError(
                "Já existe uma mesa com este número para esta empresa."
            )

        return data 

class ReservasSerializer(serializers.ModelSerializer):
    empresa = EmpresasSerializer(read_only=True)
    empresa_id = serializers.IntegerField(write_only=True)
    cliente = ClientesSerializer(read_only=True)
    cliente_id = serializers.IntegerField(write_only=True)
    quarto = QuartosSerializer(read_only=True)
    quarto_id = serializers.IntegerField(write_only=True, required=False)
    mesa = MesasSerializer(read_only=True)
    mesa_id = serializers.IntegerField(write_only=True, required=False)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Reservas
        fields = [
            'id', 'empresa', 'empresa_id', 'cliente', 'cliente_id',
            'tipo', 'tipo_display', 'quarto', 'quarto_id', 'mesa', 'mesa_id',
            'data_inicio', 'data_fim', 'status', 'status_display',
            'observacao', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        # Validação do tipo de reserva e item reservado
        tipo = data.get('tipo')
        quarto_id = data.get('quarto_id')
        mesa_id = data.get('mesa_id')

        if tipo == 'quarto' and not quarto_id:
            raise serializers.ValidationError(
                {'quarto_id': 'Quarto é obrigatório para reservas de quarto.'}
            )
        if tipo == 'mesa' and not mesa_id:
            raise serializers.ValidationError(
                {'mesa_id': 'Mesa é obrigatória para reservas de mesa.'}
            )
        if tipo == 'quarto' and mesa_id:
            raise serializers.ValidationError(
                {'mesa_id': 'Mesa não deve ser informada para reservas de quarto.'}
            )
        if tipo == 'mesa' and quarto_id:
            raise serializers.ValidationError(
                {'quarto_id': 'Quarto não deve ser informado para reservas de mesa.'}
            )

        # Validação das datas
        data_inicio = data.get('data_inicio')
        data_fim = data.get('data_fim')

        if data_fim < data_inicio:
            raise serializers.ValidationError(
                {'data_fim': 'Data de término não pode ser anterior à data de início.'}
            )

        # Verificar disponibilidade
        empresa_id = data.get('empresa_id')
        status = data.get('status', 'pendente')
        instance = getattr(self, 'instance', None)

        if tipo == 'quarto':
            reservas_existentes = Reservas.objects.filter(
                empresa_id=empresa_id,
                quarto_id=quarto_id,
                status__in=['confirmada', 'pendente'],
                data_inicio__lte=data_fim,
                data_fim__gte=data_inicio
            )
        else:
            reservas_existentes = Reservas.objects.filter(
                empresa_id=empresa_id,
                mesa_id=mesa_id,
                status__in=['confirmada', 'pendente'],
                data_inicio__lte=data_fim,
                data_fim__gte=data_inicio
            )

        if instance:
            reservas_existentes = reservas_existentes.exclude(pk=instance.pk)

        if reservas_existentes.exists():
            raise serializers.ValidationError(
                'Já existe uma reserva para este período.'
            )

        return data 