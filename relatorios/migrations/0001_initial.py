from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ResumoFolhaPagamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empresa', models.CharField(max_length=255, verbose_name='Empresa')),
                ('funcionario', models.CharField(max_length=255, verbose_name='Funcionário')),
                ('data_pagamento', models.DateField(verbose_name='Data de Pagamento')),
                ('salario_bruto', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Salário Bruto')),
                ('salario_liquido', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Salário Líquido')),
                ('inss_empresa', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='INSS Empresa')),
                ('inss_funcionario', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='INSS Funcionário')),
                ('irt', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='IRT')),
            ],
            options={
                'verbose_name': 'Resumo da Folha de Pagamento',
                'verbose_name_plural': 'Resumos da Folha de Pagamento',
                'ordering': ['empresa', 'funcionario', 'data_pagamento'],
            },
            managed=False,
            db_table='resumo_folha_pagamento',
        ),
    ] 