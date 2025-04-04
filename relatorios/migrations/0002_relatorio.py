# Generated by Django 5.1.7 on 2025-03-25 20:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relatorios', '0001_initial'),
        ('usuarios', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Relatorio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome do Relatório')),
                ('tipo', models.CharField(choices=[('vendas', 'Vendas'), ('financeiro', 'Financeiro'), ('estoque', 'Estoque'), ('rh', 'Recursos Humanos'), ('clientes', 'Clientes'), ('fornecedores', 'Fornecedores')], max_length=20, verbose_name='Tipo de Relatório')),
                ('descricao', models.TextField(verbose_name='Descrição')),
                ('formato', models.CharField(choices=[('pdf', 'PDF'), ('excel', 'Excel'), ('csv', 'CSV')], max_length=10, verbose_name='Formato')),
                ('parametros', models.JSONField(blank=True, null=True, verbose_name='Parâmetros')),
                ('arquivo', models.FileField(blank=True, null=True, upload_to='relatorios/', verbose_name='Arquivo')),
                ('data_geracao', models.DateTimeField(auto_now_add=True, verbose_name='Data de Geração')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.empresa', verbose_name='Empresa')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Relatório',
                'verbose_name_plural': 'Relatórios',
                'ordering': ['-data_geracao'],
            },
        ),
    ]
