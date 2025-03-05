# accounting_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('employees/', views.employees, name='employee-list'),
    path('vendors/', views.vendors, name='vendor-list'),
    path('customers/', views.customers, name='customer-list'),
    # path('employees/add/', views.EmployeeCreateView.as_view(), name='employee-add'),
]
