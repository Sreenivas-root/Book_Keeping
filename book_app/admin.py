from django.contrib import admin
from .models import Employee, Vendor, Customer, Invoice, PurchaseOrder

# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'address1', 'address2', 'city', 'state', 'zip', 'ssn', 'witholdings', 'salary')
    search_fields = ('first_name', 'last_name', 'address1', 'address2', 'city', 'state', 'zip', 'ssn', 'witholdings', 'salary')
    list_filter = ('first_name', 'last_name', 'city', 'state', 'zip')
    ordering = ('first_name', 'last_name', 'witholdings', 'salary')

class VendorAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'part', 'price_per_unit', 'address1', 'address2', 'city', 'state', 'zip')
    search_fields = ('company_name', 'part', 'price_per_unit', 'address1', 'address2', 'city', 'state', 'zip')
    list_filter = ('company_name', 'part', 'city', 'state', 'zip')
    ordering = ('company_name', 'part', 'price_per_unit')

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'first_name', 'last_name', 'address1', 'address2', 'city', 'state', 'zip', 'price')
    search_fields = ('company_name', 'first_name', 'last_name', 'address1', 'address2', 'city', 'state', 'zip', 'price')
    list_filter = ('company_name', 'first_name', 'last_name', 'city', 'state', 'zip')
    ordering = ('company_name', 'first_name', 'last_name', 'price')

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Customer, CustomerAdmin)