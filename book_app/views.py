from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Employee, Vendor, Customer
from django.contrib.admin.views.decorators import staff_member_required


def main(request):
  template = loader.get_template('main.html')
  return HttpResponse(template.render())

def employees(request):
  mymembers = Employee.objects.all().values()
  template = loader.get_template('employee_list.html')
  context = {
    'employee_list': mymembers,
  }
  return HttpResponse(template.render(context, request))

def vendors(request):
  mymembers = Vendor.objects.all().values()
  template = loader.get_template('vendor_list.html')
  context = {
    'vendor_list': mymembers,
  }
  return HttpResponse(template.render(context, request))

def customers(request):
  mymembers = Customer.objects.all().values()
  template = loader.get_template('customer_list.html')
  context = {
    'customer_list': mymembers,
  }
  return HttpResponse(template.render(context, request))

@staff_member_required
def employee_selection_popup(request):
    employees = Employee.objects.all()
    return render(request, 'pay_employee.html', {'employees': employees})

def pay_employee(request):
    employees = Employee.objects.all()
    return render(request, 'pay_employee_direct.html', {'employees': employees})