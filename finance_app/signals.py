from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder, Invoice, FinancialStatement

@receiver(post_save, sender=PurchaseOrder)
def update_accounts_payable(sender, instance, **kwargs):
    balance_sheet = FinancialStatement.objects.filter(statement_type='balance').latest('date')
    balance_sheet.data['liabilities']['current']['accountsPayable'] -= float(instance.total_amount)
    balance_sheet.data['assets']['current']['cash'] -= float(instance.total_amount)
    balance_sheet.save()

@receiver(post_save, sender=Invoice)
def update_accounts_receivable_and_cash(sender, instance, **kwargs):
    balance_sheet = FinancialStatement.objects.filter(statement_type='balance').latest('date')
    balance_sheet.data['assets']['current']['accountsReceivable'] -= float(instance.total_amount)
    balance_sheet.data['assets']['current']['cash'] += float(instance.total_amount)
    balance_sheet.save()
