from django.contrib import admin
from .models import Payment, PaymentTransaction, Refund, Shipment, ShipmentTracking, DeliveryStaff, DeliveryAssignment, Inventory, StockHistory, StockAdjustment, Warehouse, WarehouseInventory, InventoryAudit, Supplier, SupplierBook

admin.site.register(Payment)
admin.site.register(PaymentTransaction)
admin.site.register(Refund)
admin.site.register(Shipment)
admin.site.register(ShipmentTracking)
admin.site.register(DeliveryStaff)
admin.site.register(DeliveryAssignment)
admin.site.register(Inventory)
admin.site.register(StockHistory)
admin.site.register(StockAdjustment)
admin.site.register(Warehouse)
admin.site.register(WarehouseInventory)
admin.site.register(InventoryAudit)
admin.site.register(Supplier)
admin.site.register(SupplierBook)
