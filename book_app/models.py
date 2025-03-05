from django.db import models

# Create your models here.

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    ssn = models.CharField(max_length=100)
    witholdings = models.DecimalField(max_digits=10, decimal_places=2)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

class Vendor(models.Model):
    company_name = models.CharField(max_length=100)
    part = models.CharField(max_length=100)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    

class Customer(models.Model):
    company_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

# class Invoice(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     date = models.DateField()
#     amount = models.DecimalField(max_digits=10, decimal_places=2)

# class PurchaseOrder(models.Model):
#     vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
#     date = models.DateField()
#     quantity = models.IntegerField()
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
