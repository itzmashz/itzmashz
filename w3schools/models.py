
from django.db import models

class Category(models.Model):
  name = models.CharField(max_length=100)
  description = models.TextField(blank=True)

  def __str__(self):
      return self.name

class Shipper(models.Model):
  name = models.CharField(max_length=100)
  phone = models.CharField(max_length=20)

  def __str__(self):
      return self.name

class Supplier(models.Model):
  name = models.CharField(max_length=100)
  contact_name = models.CharField(max_length=100)
  address = models.CharField(max_length=100)
  city = models.CharField(max_length=100)
  postal_code = models.CharField(max_length=100)
  country = models.CharField(max_length=100)
  phone = models.CharField(max_length=20)

  def __str__(self):
      return self.name

class Product(models.Model):
  name = models.CharField(max_length=100)
  supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  unit = models.CharField(max_length=100)
  price = models.DecimalField(max_digits=10, decimal_places=2)

  def __str__(self):
      return self.name

class Employee(models.Model):
  last_name = models.CharField(max_length=100)
  first_name = models.CharField(max_length=100)
  birth_date = models.DateField()
  photo = models.CharField(max_length=255)
  notes = models.TextField()

  def __str__(self):
      return self.name

class Customer(models.Model):
  name = models.CharField(max_length=100)
  contact_name = models.CharField(max_length=100)
  address = models.CharField(max_length=100)
  city = models.CharField(max_length=100)
  postal_code = models.CharField(max_length=100)
  country = models.CharField(max_length=100)

  def __str__(self):
      return self.name

class Order(models.Model):
  customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
  employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
  order_date = models.DateField()
  shipper = models.ForeignKey(Shipper, on_delete=models.CASCADE)

  def __str__(self):
      return self.customer_name

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.order.customer_name} - {self.product.name}"
