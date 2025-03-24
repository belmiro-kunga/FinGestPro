from django.db import migrations

def copy_cpf_to_nif(apps, schema_editor):
    Clientes = apps.get_model('clientes', 'Clientes')
    for cliente in Clientes.objects.all():
        if not cliente.nif and cliente.cpf:
            cliente.nif = cliente.cpf
            cliente.save()

class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0002_alter_clientes_unique_together_clientes_nif_and_more'),
    ]

    operations = [
        migrations.RunPython(copy_cpf_to_nif),
    ] 