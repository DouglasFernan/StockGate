# Generated by Django 5.1.4 on 2025-01-15 16:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0010_remove_vendas_produtos_vendas_produto_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vendas",
            name="total",
            field=models.DecimalField(
                decimal_places=3, max_digits=10, verbose_name="total"
            ),
        ),
    ]
