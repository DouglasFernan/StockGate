# Generated by Django 5.1.4 on 2025-02-21 05:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0020_alter_produto_categoria"),
    ]

    operations = [
        migrations.AddField(
            model_name="vendas",
            name="cpf_cliente",
            field=models.CharField(
                default=1, max_length=11, verbose_name="CPF do Cliente"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="vendas",
            name="telefone_cliente",
            field=models.CharField(
                default=1, max_length=15, verbose_name="Telefone do Cliente"
            ),
            preserve_default=False,
        ),
    ]
