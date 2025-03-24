from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('relatorios', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE OR REPLACE VIEW resumo_folha_pagamento AS
            SELECT 
                e.nome AS empresa,
                f.nome AS funcionario,
                fp.data_pagamento,
                fp.salario_bruto,
                fp.salario_liquido,
                fp.inss_empresa,
                fp.inss_funcionario,
                fp.irt
            FROM folha_pagamento fp
            JOIN funcionarios f ON fp.funcionario_id = f.id
            JOIN empresas e ON f.empresa_id = e.id;
            """,
            reverse_sql="DROP VIEW IF EXISTS resumo_folha_pagamento;"
        ),
    ] 