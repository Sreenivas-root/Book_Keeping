from django.shortcuts import render
from .models import Account, FinancialStatement

def income_statement_view(request):
    try:
        latest_income_statement = FinancialStatement.objects.filter(statement_type='income').latest('date')
        
        latest_income_statement.data['grossProfit'] = latest_income_statement.data['sales'] - latest_income_statement.data['costOfGoodsSold']
        latest_income_statement.data['totalExpenses'] = sum(latest_income_statement.data['operatingExpenses'].values())
        latest_income_statement.data['operatingIncome'] = latest_income_statement.data['grossProfit'] - latest_income_statement.data['totalExpenses']
        latest_income_statement.data['netIncome'] = latest_income_statement.data['operatingIncome'] + latest_income_statement.data['otherIncome'] - latest_income_statement.data['incomeTaxes']
        
        context = {
            'statement': latest_income_statement.data,
            'date': latest_income_statement.date
        }
    except FinancialStatement.DoesNotExist:
        context = {'error': 'No income statement available'}
    return render(request, 'income_statement.html', context)

def balance_sheet_view(request):
    try:
        latest_balance_sheet = FinancialStatement.objects.filter(statement_type='balance').latest('date')
        
        latest_balance_sheet.data['assets']['current']['total'] = sum(latest_balance_sheet.data['assets']['current'].values())
        latest_balance_sheet.data['assets']['fixed']['total'] = sum(latest_balance_sheet.data['assets']['fixed'].values())
        latest_balance_sheet.data['liabilities']['current']['total'] = sum(latest_balance_sheet.data['liabilities']['current'].values())
        latest_balance_sheet.data['liabilities']['longTerm']['total'] = sum(latest_balance_sheet.data['liabilities']['longTerm'].values())
        
        latest_balance_sheet.data['assets']['total'] = latest_balance_sheet.data['assets']['current']['total'] + latest_balance_sheet.data['assets']['fixed']['total']
        latest_balance_sheet.data['liabilities']['total'] = latest_balance_sheet.data['liabilities']['current']['total'] + latest_balance_sheet.data['liabilities']['longTerm']['total']
        latest_balance_sheet.data['netWorth'] = latest_balance_sheet.data['assets']['total'] - latest_balance_sheet.data['liabilities']['total']
        context = {
            'statement': latest_balance_sheet.data,
            'date': latest_balance_sheet.date
        }
    except FinancialStatement.DoesNotExist:
        context = {'error': 'No balance sheet available'}
    return render(request, 'balance_sheet.html', context)
