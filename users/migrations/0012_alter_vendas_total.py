# Generated by Django 5.1.4 on 2025-01-15 16:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0011_alter_vendas_total"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vendas",
            name="total",
            field=models.DecimalField(
                decimal_places=2, max_digits=10, verbose_name="total"
            ),
        ),
    ]
