# finance_app/models.py

from django.db import models
from django.utils import timezone
from book_app.models import Employee, Vendor, Customer
from simple_history.models import HistoricalRecords

class Account(models.Model):
    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20, choices=[
        ('asset', 'Asset'),
        ('liability', 'Liability'),
        ('equity', 'Equity'),
        ('revenue', 'Revenue'),
        ('expense', 'Expense')
    ])
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    history = HistoricalRecords()

class InventoryItem(models.Model):
    part = models.CharField(max_length=100)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    reorder_point = models.IntegerField(default=0)
    history = HistoricalRecords()

    @property
    def value(self):
        return self.price_per_unit * self.quantity

class PurchaseOrder(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT)
    date = models.DateField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    history = HistoricalRecords()

class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

class Invoice(models.Model):
    customer = models.ForeignKey('book_app.Customer', on_delete=models.CASCADE, related_name='finance_invoices')
    date = models.DateField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    history = HistoricalRecords()

class InvoiceItem(models.Model):
    vendor = models.ForeignKey('book_app.Vendor', on_delete=models.CASCADE, related_name='finance_purchase_orders')
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

class PayrollPayment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    date = models.DateField(default=timezone.now)
    salary = models.DecimalField(max_digits=15, decimal_places=2)
    federal_tax = models.DecimalField(max_digits=15, decimal_places=2)
    state_tax = models.DecimalField(max_digits=15, decimal_places=2)
    social_security = models.DecimalField(max_digits=15, decimal_places=2)
    medicare = models.DecimalField(max_digits=15, decimal_places=2)
    net_pay = models.DecimalField(max_digits=15, decimal_places=2)
    history = HistoricalRecords()

class FinancialStatement(models.Model):
    date = models.DateField(default=timezone.now)
    statement_type = models.CharField(max_length=20, choices=[
        ('income', 'Income Statement'),
        ('balance', 'Balance Sheet')
    ])
    data = models.JSONField()
    history = HistoricalRecords()
