from django.urls import path
from . import views

urlpatterns = [
    path('income-statement/', views.income_statement_view, name='income_statement'),
    path('balance-sheet/', views.balance_sheet_view, name='balance_sheet'),
]
