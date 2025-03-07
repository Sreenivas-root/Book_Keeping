from django.urls import path
from . import views

urlpatterns = [
    path('income-statement/', views.income_statement_view, name='income_statement'),
    path('balance-sheet/', views.balance_sheet_view, name='balance_sheet'),
    path('pay_employee/', views.pay_employee, name='pay_employee'),
    path('financial-statement-history/', views.financial_statement_history_view, name='financial_statement_history'),
]
