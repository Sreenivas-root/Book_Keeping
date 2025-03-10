# Generated by Django 5.1.6 on 2025-03-05 01:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("company_name", models.CharField(max_length=100)),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("address1", models.CharField(max_length=100)),
                ("address2", models.CharField(max_length=100)),
                ("city", models.CharField(max_length=100)),
                ("state", models.CharField(max_length=100)),
                ("zip", models.CharField(max_length=100)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name="Employee",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                ("address1", models.CharField(max_length=100)),
                ("address2", models.CharField(max_length=100)),
                ("city", models.CharField(max_length=100)),
                ("state", models.CharField(max_length=100)),
                ("zip", models.CharField(max_length=100)),
                ("ssn", models.CharField(max_length=100)),
                ("witholdings", models.DecimalField(decimal_places=2, max_digits=10)),
                ("salary", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name="Vendor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("company_name", models.CharField(max_length=100)),
                ("part", models.CharField(max_length=100)),
                (
                    "price_per_unit",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("address1", models.CharField(max_length=100)),
                ("address2", models.CharField(max_length=100)),
                ("city", models.CharField(max_length=100)),
                ("state", models.CharField(max_length=100)),
                ("zip", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Invoice",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="book_app.customer",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PurchaseOrder",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("quantity", models.IntegerField()),
                ("total_amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "vendor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="book_app.vendor",
                    ),
                ),
            ],
        ),
    ]
