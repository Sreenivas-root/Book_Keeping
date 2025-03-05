from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Employee, Vendor, Customer, Invoice, PurchaseOrder


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


# Create your views here.

# from django.views.generic import ListView, CreateView, UpdateView, DeleteView
# from .models import Employee, Vendor, Customer, Invoice, PurchaseOrder

# class EmployeeListView(ListView):
#     model = Employee

# class EmployeeCreateView(CreateView):
#     model = Employee
#     fields = ['name', 'salary']

# Similar views for Vendor, Customer, Invoice, and PurchaseOrder
