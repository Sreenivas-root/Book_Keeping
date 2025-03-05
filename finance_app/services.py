# finance_app/services.py

from decimal import Decimal
from django.db import transaction
from .models import Account, InventoryItem, PurchaseOrder, PurchaseOrderItem, Invoice, InvoiceItem, PayrollPayment, FinancialStatement

class FinanceService:
    @staticmethod
    @transaction.atomic
    def create_purchase_order(vendor, items):
        total_amount = sum(item['quantity'] * item['price_per_unit'] for item in items)
        po = PurchaseOrder.objects.create(vendor=vendor, total_amount=total_amount)
        
        for item in items:
            inventory_item, _ = InventoryItem.objects.get_or_create(part=item['part'], defaults={'price_per_unit': item['price_per_unit']})
            PurchaseOrderItem.objects.create(
                purchase_order=po,
                inventory_item=inventory_item,
                quantity=item['quantity'],
                price_per_unit=item['price_per_unit']
            )
            inventory_item.quantity += item['quantity']
            inventory_item.save()
        
        accounts_payable = Account.objects.get(name='Accounts Payable')
        inventory = Account.objects.get(name='Inventory')
        accounts_payable.balance += total_amount
        inventory.balance += total_amount
        accounts_payable.save()
        inventory.save()
        
        return po

    @staticmethod
    @transaction.atomic
    def create_invoice(customer, items):
        total_amount = sum(item['quantity'] * item['price_per_unit'] for item in items)
        invoice = Invoice.objects.create(customer=customer, total_amount=total_amount)
        
        for item in items:
            inventory_item = InventoryItem.objects.get(part=item['part'])
            InvoiceItem.objects.create(
                invoice=invoice,
                inventory_item=inventory_item,
                quantity=item['quantity'],
                price_per_unit=item['price_per_unit']
            )
            inventory_item.quantity -= item['quantity']
            inventory_item.save()
        
        accounts_receivable = Account.objects.get(name='Accounts Receivable')
        revenue = Account.objects.get(name='Revenue')
        accounts_receivable.balance += total_amount
        revenue.balance += total_amount
        accounts_receivable.save()
        revenue.save()
        
        return invoice

    @staticmethod
    @transaction.atomic
    def process_payroll(employee, salary):
        federal_tax = Decimal('0.22') * salary
        state_tax = Decimal('0.05') * salary
        social_security = Decimal('0.062') * salary
        medicare = Decimal('0.0145') * salary
        net_pay = salary - (federal_tax + state_tax + social_security + medicare)
        
        payment = PayrollPayment.objects.create(
            employee=employee,
            salary=salary,
            federal_tax=federal_tax,
            state_tax=state_tax,
            social_security=social_security,
            medicare=medicare,
            net_pay=net_pay
        )
        
        cash = Account.objects.get(name='Cash')
        payroll_expense = Account.objects.get(name='Payroll Expense')
        cash.balance -= net_pay
        payroll_expense.balance += salary
        cash.save()
        payroll_expense.save()
        
        return payment

    @staticmethod
    def generate_income_statement():
        revenue = Account.objects.get(name='Revenue').balance
        cogs = Account.objects.get(name='Cost of Goods Sold').balance
        expenses = sum(account.balance for account in Account.objects.filter(account_type='expense'))
        net_income = revenue - cogs - expenses
        
        statement = FinancialStatement.objects.create(
            statement_type='income',
            data={
                'revenue': float(revenue),
                'cogs': float(cogs),
                'expenses': float(expenses),
                'net_income': float(net_income)
            }
        )
        return statement

    @staticmethod
    def generate_balance_sheet():
        assets = sum(account.balance for account in Account.objects.filter(account_type='asset'))
        liabilities = sum(account.balance for account in Account.objects.filter(account_type='liability'))
        equity = sum(account.balance for account in Account.objects.filter(account_type='equity'))
        
        statement = FinancialStatement.objects.create(
            statement_type='balance',
            data={
                'assets': float(assets),
                'liabilities': float(liabilities),
                'equity': float(equity)
            }
        )
        return statement
