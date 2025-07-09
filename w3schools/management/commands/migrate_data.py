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

  def load_entities(self, model, csv_file, instance_create_callback):
    Entity = model
    total_data = 0
    new_created = 0
    already_exists = 0
    with open(csv_file, 'r', encoding='utf-8') as file:
      reader = csv.DictReader(file)
      for row in reader:
        total_data += 1
        try:
          entity = Entity.objects.get(id=int(row['id']))
          already_exists += 1
        except Entity.DoesNotExist:
          entity = instance_create_callback(row)
          entity.save()
          new_created += 1
        except Exception as e:
          print(f"Error creating entity({row}): {e}")
    print(f"#> {Entity.__name__}\n\tTotal Data: {total_data}\n\tNew Created: {new_created}\n\tAlready Exists: {already_exists}")
    return total_data, new_created, already_exists

  def load_categories(self, csv_data_directory):
    csv_file = os.path.join(csv_data_directory, self.file_map['categories'])
    def create_new_category(row):
      category = Category(
          id=int(row['id']),
          name=row['name'],
          description=row['description']
      )
      category.save()
      return category
    return self.load_entities(Category, csv_file, create_new_category)

  def load_shippers(self, csv_data_directory):
      csv_file = os.path.join(csv_data_directory, self.file_map['shippers'])
      def create_new_shipper(row):
        shipper = Shipper(
            id=row['id'],
            phone=row['phone']
        )
        shipper.save()
        return shipper
      return self.load_entities(Shipper, csv_file, create_new_shipper)

  def load_suppliers(self, csv_data_directory):
    csv_file = os.path.join(csv_data_directory, self.file_map['suppliers'])
    def create_new_supplier(row):
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
      return supplier
    return self.load_entities(Supplier, csv_file, create_new_supplier)

  def load_products(self, csv_data_directory):
    csv_file = os.path.join(csv_data_directory, self.file_map['products'])
    def create_new_product(row):
        product = Product(
          id=row['id'],
          name=row['name'],
          supplier=Supplier.objects.get(id=int(row['supplier_id'])),
          category=Category.objects.get(id=int(row['category_id'])),
          unit=row['unit'],
          price=Decimal(row['price'])
        )
        product.save()
        return product
    return self.load_entities(Product, csv_file, create_new_product)

  def load_employees(self, csv_data_directory):
    csv_file = os.path.join(csv_data_directory, self.file_map['employees'])
    def create_new_employee(row):
      employee = Employee(
        id=row['id'],
        last_name=row['last_name'],
        first_name=row['first_name'],
        birth_date=dt.strptime(row['birth_date'], '%Y-%m-%d'),
        photo=row['photo'],
        notes=row['notes'],
      )
      employee.save()
      return employee
    return self.load_entities(Employee, csv_file, create_new_employee)

  def load_customers(self, csv_data_directory):
    csv_file = os.path.join(csv_data_directory, self.file_map['customers'])
    def create_new_customer(row):
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
      return customer
    return self.load_entities(Customer, csv_file, create_new_customer)

  def load_orders(self, csv_data_directory):
    csv_file = os.path.join(csv_data_directory, self.file_map['orders'])
    def create_new_order(row):
      order = Order(
        id=row['id'],
        customer=Customer.objects.get(id=int(row['customer_id'])),
        employee=Employee.objects.get(id=int(row['employee_id'])),
        order_date=dt.strptime(row['order_date'], '%Y-%m-%d'),
        shipper=Shipper.objects.get(id=int(row['shipper_id'])),
      )
      order.save()
      return order
    return self.load_entities(Order, csv_file, create_new_order)

  def load_order_details(self, csv_data_directory):
    csv_file = os.path.join(csv_data_directory, self.file_map['order_details'])
    def create_new_order_detail(row):
      product =Product.objects.get(id=int(row['product_id']))
      order_detail = OrderDetail(
        id=row['id'],
        order=Order.objects.get(id=int(row['order_id'])),
        product=product,
        quantity=int(row['quantity']),
        unit_price=product.price
      )
      order_detail.save()
      return order_detail
    return self.load_entities(OrderDetail, csv_file, create_new_order_detail)

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
