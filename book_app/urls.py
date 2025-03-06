# accounting_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('employees/', views.employees, name='employee-list'),
    path('vendors/', views.vendors, name='vendor-list'),
    path('customers/', views.customers, name='customer-list'),
    path('admin/employee-selection-popup/', views.employee_selection_popup, name='employee_selection_popup'),
    # path('employees/add/', views.EmployeeCreateView.as_view(), name='employee-add'),
]
