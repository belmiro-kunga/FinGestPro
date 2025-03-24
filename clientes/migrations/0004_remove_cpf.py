from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0003_copy_cpf_to_nif'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientes',
            name='cpf',
        ),
    ] 