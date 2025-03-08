# accounting_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('employees/', views.employees, name='employee-list'),
    path('vendors/', views.vendors, name='vendor-list'),
    path('customers/', views.customers, name='customer-list'),
    path('pay-employee/', views.pay_employee, name='pay_employee'),
    path('admin/employee-selection-popup/', views.employee_selection_popup, name='employee_selection_popup'),
]
