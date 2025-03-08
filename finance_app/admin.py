from django.contrib import admin
from .models import Account, FinancialStatement, InventoryItem, PurchaseOrder, PurchaseOrderItem, Invoice, PayrollPayment, InventoryCount

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('customer', 'date', 'quantity', 'price', 'total_amount')
    ordering = ('customer', 'date', 'quantity')

    def price(self, obj):
        return obj.price

    def total_amount(self, obj):
        return obj.total_amount

    price.admin_order_field = 'customer__price'
    total_amount.admin_order_field = 'quantity'


# Register your models here.
admin.site.register(Account)
admin.site.register(FinancialStatement)
admin.site.register(InventoryItem)
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderItem)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(PayrollPayment)
admin.site.register(InventoryCount)

