# Generated by Django 5.1.6 on 2025-03-05 04:51

import django.db.models.deletion
import django.utils.timezone
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("book_app", "0002_remove_purchaseorder_vendor_delete_invoice_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Account",
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
                ("name", models.CharField(max_length=100)),
                (
                    "account_type",
                    models.CharField(
                        choices=[
                            ("asset", "Asset"),
                            ("liability", "Liability"),
                            ("equity", "Equity"),
                            ("revenue", "Revenue"),
                            ("expense", "Expense"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "balance",
                    models.DecimalField(decimal_places=2, default=0, max_digits=15),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FinancialStatement",
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
                ("date", models.DateField(default=django.utils.timezone.now)),
                (
                    "statement_type",
                    models.CharField(
                        choices=[
                            ("income", "Income Statement"),
                            ("balance", "Balance Sheet"),
                        ],
                        max_length=20,
                    ),
                ),
                ("data", models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name="InventoryItem",
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
                ("part", models.CharField(max_length=100)),
                (
                    "price_per_unit",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("quantity", models.IntegerField(default=0)),
                ("reorder_point", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="HistoricalAccount",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "account_type",
                    models.CharField(
                        choices=[
                            ("asset", "Asset"),
                            ("liability", "Liability"),
                            ("equity", "Equity"),
                            ("revenue", "Revenue"),
                            ("expense", "Expense"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "balance",
                    models.DecimalField(decimal_places=2, default=0, max_digits=15),
                ),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "historical account",
                "verbose_name_plural": "historical accounts",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="HistoricalFinancialStatement",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
                    ),
                ),
                ("date", models.DateField(default=django.utils.timezone.now)),
                (
                    "statement_type",
                    models.CharField(
                        choices=[
                            ("income", "Income Statement"),
                            ("balance", "Balance Sheet"),
                        ],
                        max_length=20,
                    ),
                ),
                ("data", models.JSONField()),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "historical financial statement",
                "verbose_name_plural": "historical financial statements",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="HistoricalInventoryItem",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
                    ),
                ),
                ("part", models.CharField(max_length=100)),
                (
                    "price_per_unit",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("quantity", models.IntegerField(default=0)),
                ("reorder_point", models.IntegerField(default=0)),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "historical inventory item",
                "verbose_name_plural": "historical inventory items",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="HistoricalInvoice",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
                    ),
                ),
                ("date", models.DateField(default=django.utils.timezone.now)),
                ("total_amount", models.DecimalField(decimal_places=2, max_digits=15)),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="book_app.customer",
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "historical invoice",
                "verbose_name_plural": "historical invoices",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="HistoricalPayrollPayment",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
                    ),
                ),
                ("date", models.DateField(default=django.utils.timezone.now)),
                ("salary", models.DecimalField(decimal_places=2, max_digits=15)),
                ("federal_tax", models.DecimalField(decimal_places=2, max_digits=15)),
                ("state_tax", models.DecimalField(decimal_places=2, max_digits=15)),
                (
                    "social_security",
                    models.DecimalField(decimal_places=2, max_digits=15),
                ),
                ("medicare", models.DecimalField(decimal_places=2, max_digits=15)),
                ("net_pay", models.DecimalField(decimal_places=2, max_digits=15)),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "employee",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="book_app.employee",
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "historical payroll payment",
                "verbose_name_plural": "historical payroll payments",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="HistoricalPurchaseOrder",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
                    ),
                ),
                ("date", models.DateField(default=django.utils.timezone.now)),
                ("total_amount", models.DecimalField(decimal_places=2, max_digits=15)),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "vendor",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="book_app.vendor",
                    ),
                ),
            ],
            options={
                "verbose_name": "historical purchase order",
                "verbose_name_plural": "historical purchase orders",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
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
                ("date", models.DateField(default=django.utils.timezone.now)),
                ("total_amount", models.DecimalField(decimal_places=2, max_digits=15)),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="finance_invoices",
                        to="book_app.customer",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="InvoiceItem",
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
                ("quantity", models.IntegerField()),
                (
                    "price_per_unit",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "inventory_item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="finance_app.inventoryitem",
                    ),
                ),
                (
                    "vendor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="finance_purchase_orders",
                        to="book_app.vendor",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PayrollPayment",
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
                ("date", models.DateField(default=django.utils.timezone.now)),
                ("salary", models.DecimalField(decimal_places=2, max_digits=15)),
                ("federal_tax", models.DecimalField(decimal_places=2, max_digits=15)),
                ("state_tax", models.DecimalField(decimal_places=2, max_digits=15)),
                (
                    "social_security",
                    models.DecimalField(decimal_places=2, max_digits=15),
                ),
                ("medicare", models.DecimalField(decimal_places=2, max_digits=15)),
                ("net_pay", models.DecimalField(decimal_places=2, max_digits=15)),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="book_app.employee",
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
                ("date", models.DateField(default=django.utils.timezone.now)),
                ("total_amount", models.DecimalField(decimal_places=2, max_digits=15)),
                (
                    "vendor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="book_app.vendor",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PurchaseOrderItem",
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
                ("quantity", models.IntegerField()),
                (
                    "price_per_unit",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "inventory_item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="finance_app.inventoryitem",
                    ),
                ),
                (
                    "purchase_order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="finance_app.purchaseorder",
                    ),
                ),
            ],
        ),
    ]
