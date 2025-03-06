from django.contrib import admin
from .models import Employee, Vendor, Customer
from django.urls import path
from django.http import HttpResponseRedirect

# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    change_list_template = 'employee_changelist.html'
    list_display = ('first_name', 'last_name', 'address1', 'address2', 'city', 'state', 'zip', 'ssn', 'witholdings', 'salary')
    search_fields = ('first_name', 'last_name', 'address1', 'address2', 'city', 'state', 'zip', 'ssn', 'witholdings', 'salary')
    list_filter = ('first_name', 'last_name', 'city', 'state', 'zip')
    ordering = ('first_name', 'last_name', 'witholdings', 'salary')
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('custom_action/', self.custom_action),
        ]
        return custom_urls + urls

    def custom_action(self, request):
        # Implement your custom action here
        self.message_user(request, "Custom action performed")
        return HttpResponseRedirect("../")
    class Media:
        js = ('js/employee_selection.js',)

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