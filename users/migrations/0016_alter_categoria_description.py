# Generated by Django 5.1.4 on 2025-02-03 18:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0015_alter_produto_price_alter_produto_quantity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="categoria",
            name="description",
            field=models.TextField(verbose_name="description"),
        ),
    ]
