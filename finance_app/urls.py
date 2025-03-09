from django.urls import path
from . import views

urlpatterns = [
    path('income-statement/', views.income_statement_view, name='income_statement'),
    path('balance-sheet/', views.balance_sheet_view, name='balance_sheet'),
    path('pay_employee/', views.pay_employee, name='pay_employee'),
    path('financial-statement-history/', views.financial_statement_history_view, name='financial_statement_history'),
    path('simulate/accounts_receivable_and_cash/<int:invoice_id>/', views.simulate_accounts_receivable_and_cash_view, name='simulate_accounts_receivable_and_cash'),
    path('simulate/accounts_payable/<int:purchase_order_id>/', views.simulate_accounts_payable_view, name='simulate_accounts_payable'),
    path('simulate/list/', views.simulation_list_view, name='simulation_list'),
]
