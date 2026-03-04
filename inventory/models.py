from django.db import models
from sales.models import Order
from catalog.models import Book
from users.models import Address, Member

class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    method = models.CharField(max_length=50) # e.g., Credit Card, PayPal, COD
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)

class PaymentTransaction(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='transactions')
    gateway = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=255)
    status = models.CharField(max_length=50)

class Refund(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    refunded_at = models.DateTimeField(auto_now_add=True)

class Shipment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    shipped_at = models.DateTimeField(null=True, blank=True)

class ShipmentTracking(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='tracking_logs')
    status = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now_add=True)

class DeliveryStaff(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)

class DeliveryAssignment(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    staff = models.ForeignKey(DeliveryStaff, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

class Inventory(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

class StockHistory(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    change_amount = models.IntegerField()
    changed_at = models.DateTimeField(auto_now_add=True)

class StockAdjustment(models.Model):
    staff = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    before_qty = models.IntegerField()
    after_qty = models.IntegerField()
    reason = models.TextField()
    adjusted_at = models.DateTimeField(auto_now_add=True)

class Warehouse(models.Model):
    name = models.CharField(max_length=255)
    location = models.TextField()

class WarehouseInventory(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

class InventoryAudit(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    checked_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

class SupplierBook(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
