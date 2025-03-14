# Generated by Django 5.1.4 on 2025-02-24 08:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0027_alter_customuser_cpf"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vendas",
            name="cliente",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="users.cliente",
                verbose_name="cliente",
            ),
        ),
        migrations.AlterField(
            model_name="vendas",
            name="produto",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="users.produto",
                verbose_name="produto",
            ),
        ),
        migrations.AlterField(
            model_name="vendas",
            name="vendedor",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to=settings.AUTH_USER_MODEL,
                verbose_name="vendedor",
            ),
        ),
    ]
