from django.db import migrations, models

def create_initial_data(apps, schema_editor):
    Employee = apps.get_model('book_app', 'Employee')
    Vendor = apps.get_model('book_app', 'Vendor')
    Customer = apps.get_model('book_app', 'Customer')

    # Create initial Employees
    Employee.objects.create(
        first_name='John', last_name='Doe', address1='123 Elm St', address2='', city='Springfield',
        state='IL', zip='62701', ssn='123-45-6789', witholdings=1, salary=60000.00
    )
    Employee.objects.create(
        first_name='Jane', last_name='Smith', address1='456 Oak St', address2='Apt 2', city='Springfield',
        state='IL', zip='62702', ssn='987-65-4321', witholdings=2, salary=65000.00
    )

    # Create initial Vendors
    Vendor.objects.create(
        company_name='ABC Supplies', part='Widget', price_per_unit=10.00, address1='789 Pine St', address2='',
        city='Springfield', state='IL', zip='62703'
    )
    Vendor.objects.create(
        company_name='XYZ Tools', part='Gadget', price_per_unit=15.00, address1='101 Maple St', address2='Suite 100',
        city='Springfield', state='IL', zip='62704'
    )

    # Create initial Customers
    Customer.objects.create(
        company_name='Acme Corp', first_name='Alice', last_name='Johnson', address1='202 Birch St', address2='',
        city='Springfield', state='IL', zip='62705', price=1000.00
    )
    Customer.objects.create(
        company_name='Global Industries', first_name='Bob', last_name='Brown', address1='303 Cedar St', address2='',
        city='Springfield', state='IL', zip='62706', price=1500.00
    )

class Migration(migrations.Migration):

    dependencies = [
        ('book_app', '0002_remove_purchaseorder_vendor_delete_invoice_and_more'),
    ]

    operations = [
        migrations.RunPython(create_initial_data),
    ]
