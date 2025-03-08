from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import FinancialStatement, PayrollPayment
from book_app.models import Employee
import logging
from decimal import Decimal
from datetime import date
from django.utils import timezone

logger = logging.getLogger(__name__)

def income_statement_view(request):
    try:
        latest_income_statement = FinancialStatement.objects.filter(statement_type='income').latest('date')
        
        latest_income_statement.data['grossProfit'] = latest_income_statement.data['sales'] - latest_income_statement.data['costOfGoodsSold']
        latest_income_statement.data['totalExpenses'] = sum(latest_income_statement.data['operatingExpenses'].values())
        latest_income_statement.data['operatingIncome'] = latest_income_statement.data['grossProfit'] - latest_income_statement.data['totalExpenses']
        latest_income_statement.data['netIncome'] = latest_income_statement.data['operatingIncome'] + latest_income_statement.data['otherIncome'] - latest_income_statement.data['incomeTaxes']
        
        context = {
            'statement': latest_income_statement.data,
            'date': date.today()
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
            'date': date.today()
        }
    except FinancialStatement.DoesNotExist:
        context = {'error': 'No balance sheet available'}
    return render(request, 'balance_sheet.html', context)


def financial_statement_history_view(request):
    historical_records = FinancialStatement.history.all()
    context = {
        'historical_records': historical_records
    }
    return render(request, 'financial_statement_history.html', context)


def decimal_to_float(data):
    if isinstance(data, dict):
        return {k: decimal_to_float(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [decimal_to_float(i) for i in data]
    elif isinstance(data, Decimal):
        return float(data)
    return data

def pay_employee(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee')

        if employee_id:
            try:
                employee = Employee.objects.get(id=employee_id)
                salary = employee.salary

                # Calculate tax values (example rates)
                federal_tax_rate = Decimal('0.10')
                state_tax_rate = Decimal('0.05')
                social_security_rate = Decimal('0.062')
                medicare_rate = Decimal('0.0145')

                federal_tax = salary * federal_tax_rate
                state_tax = salary * state_tax_rate
                social_security = salary * social_security_rate
                medicare = salary * medicare_rate
                net_pay = salary - (federal_tax + state_tax + social_security + medicare)

                # Create a payroll payment record
                payroll_payment = PayrollPayment(
                    employee=employee,
                    salary=float(salary),
                    federal_tax=float(federal_tax),
                    state_tax=float(state_tax),
                    social_security=float(social_security),
                    medicare=float(medicare),
                    net_pay=float(net_pay),
                    date=timezone.now()
                )
                payroll_payment.save()

                # Update the income statement
                latest_income_statement = FinancialStatement.objects.filter(statement_type='income').latest('date')
                latest_income_statement.data['operatingExpenses']['payroll'] += float(net_pay)
                latest_income_statement.data['operatingExpenses']['payrollWitholding'] += float(federal_tax + state_tax + social_security + medicare)
                latest_income_statement.data = decimal_to_float(latest_income_statement.data)
                latest_income_statement.save()

                # Update the balance sheet
                latest_balance_sheet = FinancialStatement.objects.filter(statement_type='balance').latest('date')
                latest_balance_sheet.data['assets']['current']['cash'] -= float(salary)
                latest_balance_sheet.data = decimal_to_float(latest_balance_sheet.data)
                latest_balance_sheet.save()

                return JsonResponse({'success': True})

            except Employee.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Employee not found'})
            except FinancialStatement.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Financial statement not found'})
            except Exception as e:
                logger.error(f'Unexpected error: {e}')
                return JsonResponse({'success': False, 'error': 'An unexpected error occurred'})

        return JsonResponse({'success': False, 'error': 'Invalid employee ID'})

    # employees = Employee.objects.all()
    # return render(request, 'pay_employee.html', {'employees': employees})