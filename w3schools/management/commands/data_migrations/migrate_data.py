import os
import csv
from decimal import Decimal
from datetime import datetime as dt
from w3schools.models import *
from django.core.management.base import BaseCommand

class Command(BaseCommand):
  help = 'Import data from CSV file'
  file_map = {
    'categories': 'categories.csv',
    'customers': 'customers.csv',
    'employees': 'employees.csv',
    'orders': 'orders.csv',
    'order_details': 'order_details.csv',
    'products': 'products.csv',
    'suppliers': 'suppliers.csv',
    'shippers': 'shippers.csv'
  }
  def add_arguments(self, parser):
    parser.add_argument('csv_data_directory', type=str, help='Directory Path to CSV files')
    parser.add_argument('--confirm', action='store_true', help='Confirm Migration')

  def load_categories(self, csv_data_directory):
    csv_file = os.path.join(csv_data_directory, self.file_map['categories'])
    with open(csv_file, 'r', encoding='utf-8') as file:
      reader = csv.DictReader(file)
      for row in reader:
        category = Category(
            id=row['id'],
            category_name=row['name'],
            description=row['description']
        )
        category.save()

  def load_shippers(self, csv_data_directory):
      csv_file = os.path.join(csv_data_directory, self.file_map['shippers'])
      with open(csv_file, 'r', encoding='utf-8') as file:
          reader = csv.DictReader(file)
          for row in reader:
              shipper = Shipper(
                  id=row['id'],
                  phone=row['phone']
              )
              shipper.save()

  def load_suppliers(self, csv_data_directory):
    csv_file = os.path.join(csv_data_directory, self.file_map['suppliers'])
    with open(csv_file, 'r', encoding='utf-8') as file:
      reader = csv.DictReader(file)
      for row in reader:
        supplier = Supplier(
          id=row['id'],
          contact_name=row['contact_name'],
          address=row['address'],
          city=row['city'],
          postal_code=row['postal_code'],
          country=row['country'],
          phone=row['phone'],
        )
        supplier.save()

  def load_products(self, csv_data_directory):
    csv_file = os.path.join(csv_data_directory, self.file_map['products'])
    with open(csv_file, 'r', encoding='utf-8') as file:
      reader = csv.DictReader(file)
      for row in reader:
        product = Product(
          id=row['id'],
          name=row['name'],
          supplier=Supplier.objects.get(id=int(row['supplier_id'])),
          category=Category.objects.get(id=int(row['category_id'])),
          unit=row['unit'],
          price=Decimal(row['price'])
        )
        product.save()

  def load_employees(self, csv_data_directory):
    csv_file = os.path.join(csv_data_directory, self.file_map['employees'])
    with open(csv_file, 'r', encoding='utf-8') as file:
      reader = csv.DictReader(file)
      for row in reader:
        employee = Employee(
          id=row['id'],
          last_name=row['last_name'],
          first_name=row['first_name'],
          birth_date=dt.strptime(row['birth_date'], '%Y-%m-%d'),
          photo=row['photo'],
          notes=row['notes'],
        )
        employee.save()


  def load_customers(self, csv_data_directory):
    csv_file = os.path.join(csv_data_directory, self.file_map['customers'])
    with open(csv_file, 'r', encoding='utf-8') as file:
      reader = csv.DictReader(file)
      for row in reader:
        customer = Customer(
          id=row['id'],
          name=row['name'],
          contact_name=row['contact_name'],
          address=row['address'],
          city=row['city'],
          postal_code=row['postal_code'],
          country=row['country'],
        )
        customer.save()


  def load_orders(self, csv_data_directory):
    csv_file = os.path.join(csv_data_directory, self.file_map['orders'])
    with open(csv_file, 'r', encoding='utf-8') as file:
      reader = csv.DictReader(file)
      for row in reader:
        order = Order(
          id=row['id'],
          customer=Customer.objects.get(id=int(row['customer_id'])),
          employee=Employee.objects.get(id=int(row['employee_id'])),
          order_date=datetime.strptime(row['order_date'], '%Y-%m-%d %H:%M:%S'),
          shipper=Shipper.objects.get(id=int(row['shipper_id'])),
        )
        order.save()

  def load_order_details(self, csv_data_directory):
    csv_file = os.path.join(csv_data_directory, self.file_map['order_details'])
    with open(csv_file, 'r', encoding='utf-8') as file:
      reader = csv.DictReader(file)
      for row in reader:
        order_detail = OrderDetail(
          id=row['id'],
          order=Order.objects.get(id=int(row['order_id'])),
          product=Product.objects.get(id=int(row['product_id'])),
          quantity=int(row['quantity']),
          unit_price=Decimal(row['unit_price'])
        )
        order_detail.save()

  def handle(self, *args, **options):
    csv_data_directory = options['csv_data_directory']
    if options['confirm']:
      print(f"loading categories..")
      self.load_categories(csv_data_directory)
      print(f"loading shippers..")
      self.load_shippers(csv_data_directory)
      print(f"loading suppliers..")
      self.load_suppliers(csv_data_directory)
      print(f"loading products..")
      self.load_products(csv_data_directory)
      print(f"loading employees..")
      self.load_employees(csv_data_directory)
      print(f"loading customers..")
      self.load_customers(csv_data_directory)
      print(f"loading orders..")
      self.load_orders(csv_data_directory)
      print(f"loading order details..")
      self.load_order_details(csv_data_directory)
    else:
      print("Please Confirm Migration")
    print("Migration completed.")
