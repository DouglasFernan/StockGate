# Generated by Django 5.1.4 on 2025-02-21 23:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0022_alter_vendas_total"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cliente",
            name="cep",
        ),
        migrations.AddField(
            model_name="cliente",
            name="complemento",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="complemento"
            ),
        ),
        migrations.AlterField(
            model_name="vendas",
            name="cpf_cliente",
            field=models.CharField(
                max_length=14,
                validators=[
                    django.core.validators.RegexValidator(
                        message="O CPF deve estar no formato XXX.XXX.XXX-XX.",
                        regex="^\\d{3}\\.\\d{3}\\.\\d{3}-\\d{2}$",
                    )
                ],
                verbose_name="CPF do Cliente",
            ),
        ),
        migrations.AlterField(
            model_name="vendas",
            name="quantity",
            field=models.PositiveIntegerField(
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(1000),
                ],
                verbose_name="quantity",
            ),
        ),
        migrations.AlterField(
            model_name="vendas",
            name="telefone_cliente",
            field=models.CharField(
                max_length=15,
                validators=[
                    django.core.validators.RegexValidator(
                        message="O telefone deve estar no formato (XX) XXXXX-XXXX.",
                        regex="^\\(\\d{2}\\) \\d{5}-\\d{4}$",
                    )
                ],
                verbose_name="Telefone do Cliente",
            ),
        ),
        migrations.AlterField(
            model_name="vendas",
            name="total",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=10,
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
                verbose_name="total",
            ),
        ),
    ]
