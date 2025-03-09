from django.db import migrations
from django.utils import timezone

def populate_initial_data(apps, schema_editor):
    FinancialStatement = apps.get_model('finance_app', 'FinancialStatement')
    InventoryCount = apps.get_model('finance_app', 'InventoryCount')
    InventoryItem = apps.get_model('finance_app', 'InventoryItem')
    Vendor = apps.get_model('book_app', 'Vendor')
    
    # Create initial income statement
    FinancialStatement.objects.create(
        date=timezone.now(),
        statement_type='income',
        data={
            "sales": 0,
            "costOfGoodsSold": 0,
            "operatingExpenses": {
                "payroll": 0,
                "payrollWitholding": 0,
                "rent": 0,
                "bills": 0,
                "miscellaneous": 0,
                "annualExpenses": 10000
            },
            "otherIncome": 0,
            "incomeTaxes": 0
        }
    )
    
    # Create initial balance sheet
    FinancialStatement.objects.create(
        date=timezone.now(),
        statement_type='balance',
        data={
            "assets": {
                "current": {
                    "cash": 200000,
                    "accountsReceivable": 0,
                    "inventory": 0
                },
                "fixed": {
                    "land": 0,
                    "building": 0,
                    "equipment": 0,
                    "furniture": 0
                }
            },
            "liabilities": {
                "current": {
                    "accountsPayable": 0,
                    "notesPayable": 0,
                    "accruals": 0
                },
                "longTerm": {
                    "mortgage": 0
                }
            }
        }
    )

    InventoryCount.objects.create(
        date=timezone.now(),
        quantity=100
    )

    # Create initial InventoryItems
    vendor1 = Vendor.objects.get(company_name='ABC Supplies')
    vendor2 = Vendor.objects.get(company_name='XYZ Tools')
    
    InventoryItem.objects.create(
        vendor=vendor1,
        quantity=50,
        reorder_point=False
    )
    InventoryItem.objects.create(
        vendor=vendor2,
        quantity=30,
        reorder_point=True
    )

class Migration(migrations.Migration):

    dependencies = [
        ('finance_app', '0006_alter_purchaseorder_inventory_item'),
    ]

    operations = [
        migrations.RunPython(populate_initial_data),
    ]