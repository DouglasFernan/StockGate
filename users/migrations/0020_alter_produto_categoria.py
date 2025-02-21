# Generated by Django 5.1.4 on 2025-02-21 00:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0019_alter_produto_categoria"),
    ]

    operations = [
        migrations.AlterField(
            model_name="produto",
            name="categoria",
            field=models.ForeignKey(
                default=4,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                to="users.categoria",
                verbose_name="Categoria",
            ),
        ),
    ]
