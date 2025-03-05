from django.contrib import admin
from .models import Account, FinancialStatement, InventoryItem, PurchaseOrder, PurchaseOrderItem, Invoice, InvoiceItem, PayrollPayment

# Register your models here.
admin.site.register(Account)
admin.site.register(FinancialStatement)
admin.site.register(InventoryItem)
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderItem)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)
admin.site.register(PayrollPayment)