from django.contrib import admin
from .models import FinancialStatement, InventoryItem, PurchaseOrder, Invoice, PayrollPayment, InventoryCount

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('date', 'customer', 'quantity', 'price', 'total_amount')
    ordering = ('-date', 'customer', 'quantity')

    def price(self, obj):
        return obj.price

    def total_amount(self, obj):
        return obj.total_amount

    price.admin_order_field = 'customer__price'
    total_amount.admin_order_field = 'quantity'

class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('date', 'supplier', 'inventory_item', 'quantity', 'price_per_unit', 'total_amount')
    ordering = ('-date', 'inventory_item', 'quantity')

    def price_per_unit(self, obj):
        return obj.price_per_unit

    def total_amount(self, obj):
        return obj.total_amount
    
    def supplier(self, obj):
        return obj.inventory_item.vendor

    price_per_unit.admin_order_field = 'inventory_item__price_per_unit'
    total_amount.admin_order_field = 'quantity'

class InventoryCountAdmin(admin.ModelAdmin):
    list_display = ('date', 'quantity')

class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('part', 'price_per_unit', 'quantity', 'value', 'reorder_point')
    ordering = ('vendor', 'quantity')

    def part(self, obj):
        return obj.part

    def price_per_unit(self, obj):
        return obj.price_per_unit
    
    def value(self, obj):
        return obj.value

    part.admin_order_field = 'part'
    price_per_unit.admin_order_field = 'price_per_unit'
    value.admin_order_field = 'value'


class PayrollPaymentAdmin(admin.ModelAdmin):
    list_display = ('date', 'employee', 'salary', 'federal_tax', 'state_tax', 'social_security', 'medicare', 'deductions', 'net_pay')
    ordering = ('-date', 'employee')

    def deductions(self, obj):
        return obj.deductions

# Register your models here.
admin.site.register(FinancialStatement)
admin.site.register(InventoryItem, InventoryItemAdmin)
admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(PayrollPayment, PayrollPaymentAdmin)
admin.site.register(InventoryCount, InventoryCountAdmin)

