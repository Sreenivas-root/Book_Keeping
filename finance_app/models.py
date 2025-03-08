# finance_app/models.py

from django.db import models
from django.utils import timezone
from book_app.models import Employee, Vendor, Customer
from simple_history.models import HistoricalRecords
from decimal import Decimal

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
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=0)
    reorder_point = models.IntegerField(default=0)
    history = HistoricalRecords()

    def __str__(self):
        return self.vendor.part

    @property
    def part(self):
        return self.vendor.part if self.vendor else None

    @property
    def price_per_unit(self):
        return self.vendor.price_per_unit if self.vendor else None

    @property
    def value(self):
        return self.price_per_unit * self.quantity if self.price_per_unit else 0

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
    quantity = models.DecimalField(max_digits=15, decimal_places=2)
    history = HistoricalRecords()

    @property
    def price(self):
        return self.customer.price
    
    @property
    def total_amount(self):
        return self.quantity * self.price

    def save(self, *args, **kwargs):
        income_statement = FinancialStatement.objects.filter(statement_type='income').latest('date')
        balance_sheet = FinancialStatement.objects.filter(statement_type='balance').latest('date')
        inventory_count = InventoryCount.objects.latest('date')
        if inventory_count.quantity >= self.quantity:
            inventory_count.quantity -= self.quantity
        else:
            self.quantity = inventory_count.quantity
            inventory_count.quantity = 0
        cogs = sum(vendor.price_per_unit for vendor in Vendor.objects.all()) * Decimal(self.quantity)
        balance_sheet.data['assets']['current']['accountsReceivable'] += float(self.quantity) * float(self.price)
        income_statement.data['costOfGoodsSold'] += float(cogs)
        income_statement.data['sales'] += float(self.quantity) * float(self.price)
        inventory_count.save()
        income_statement.save()
        balance_sheet.save()
        super().save(*args, **kwargs)

class InventoryCount(models.Model):
    date = models.DateField(default=timezone.now)
    quantity = models.IntegerField()
    history = HistoricalRecords()

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

    def __str__(self):
        return self.statement_type == 'income' and 'Income Statement' or 'Balance Sheet'
