# Generated by Django 5.1.7 on 2025-03-25 20:47

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fornecedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200, verbose_name='Nome/Razão Social')),
                ('tipo', models.CharField(choices=[('empresa', 'Empresa'), ('individual', 'Individual'), ('associacao', 'Associação'), ('cooperativa', 'Cooperativa'), ('outros', 'Outros')], max_length=20, verbose_name='Tipo de Fornecedor')),
                ('nif', models.CharField(help_text='Número de Identificação Fiscal', max_length=20, unique=True, verbose_name='NIF')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('telefone', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message='Número de telefone deve ser inserido no formato: "+999999999"', regex='^\\+?1?\\d{9,15}$')], verbose_name='Telefone')),
                ('endereco', models.TextField(verbose_name='Endereço')),
                ('cidade', models.CharField(max_length=100, verbose_name='Cidade')),
                ('estado', models.CharField(max_length=2, verbose_name='Estado')),
                ('cep', models.CharField(max_length=8, validators=[django.core.validators.RegexValidator(message='CEP deve conter 8 dígitos', regex='^\\d{8}$')], verbose_name='CEP')),
                ('website', models.URLField(blank=True, null=True, verbose_name='Website')),
                ('observacoes', models.TextField(blank=True, null=True, verbose_name='Observações')),
                ('ativo', models.BooleanField(default=True, verbose_name='Fornecedor Ativo')),
                ('data_cadastro', models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')),
                ('data_atualizacao', models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.empresa', verbose_name='Empresa')),
            ],
            options={
                'verbose_name': 'Fornecedor',
                'verbose_name_plural': 'Fornecedores',
                'ordering': ['nome'],
                'unique_together': {('empresa', 'nif')},
            },
        ),
    ]
