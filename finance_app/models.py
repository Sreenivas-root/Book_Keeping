# finance_app/models.py

from django.db import models
from django.utils import timezone
from book_app.models import Employee, Vendor, Customer
from simple_history.models import HistoricalRecords
from decimal import Decimal
from django.utils.timezone import now
from datetime import timedelta
from celery import shared_task

class InventoryItem(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=0)
    reorder_point = models.BooleanField(default=False)
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
    date = models.DateField(default=timezone.now)
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=0)
    history = HistoricalRecords()

    @property
    def price_per_unit(self):
        return self.inventory_item.price_per_unit if self.inventory_item else None
    
    @property
    def total_amount(self):
        return self.price_per_unit * self.quantity if self.price_per_unit else 0
    
    def save(self, *args, **kwargs):
        balance_sheet = FinancialStatement.objects.filter(statement_type='balance').latest('date')
        balance_sheet.data['liabilities']['current']['accountsPayable'] += float(self.total_amount)
        InventoryItem.objects.filter(pk=self.inventory_item.pk).update(quantity=self.inventory_item.quantity + self.quantity)
        balance_sheet.save()
        super().save(*args, **kwargs)
        # Schedule the update of accountsPayable and cash after 30 days
        update_accounts_payable.apply_async((self.pk,), eta=now() + timedelta(days=30))

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
        # Schedule the update of accountsReceivable and cash after 30 days
        update_accounts_receivable_and_cash.apply_async((self.pk,), eta=now() + timedelta(days=30))

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

    @property
    def deductions(self):
        return self.federal_tax + self.state_tax + self.social_security + self.medicare

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

@shared_task
def update_accounts_receivable_and_cash(invoice_id):
    try:
        invoice = Invoice.objects.get(pk=invoice_id)
        balance_sheet = FinancialStatement.objects.filter(statement_type='balance').latest('date')
        balance_sheet.data['assets']['current']['accountsReceivable'] -= float(invoice.total_amount)
        balance_sheet.data['assets']['current']['cash'] += float(invoice.total_amount)
        balance_sheet.save()
    except Invoice.DoesNotExist:
        pass


@shared_task
def update_accounts_payable(purchase_order_id):
    try:
        purchase_order = PurchaseOrder.objects.get(pk=purchase_order_id)
        balance_sheet = FinancialStatement.objects.filter(statement_type='balance').latest('date')
        balance_sheet.data['liabilities']['current']['accountsPayable'] -= float(purchase_order.total_amount)
        balance_sheet.data['assets']['current']['cash'] -= float(purchase_order.total_amount)
        balance_sheet.save()
    except PurchaseOrder.DoesNotExist:
        pass