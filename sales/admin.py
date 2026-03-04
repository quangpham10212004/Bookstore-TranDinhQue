from django.contrib import admin
from .models import Wishlist, WishlistItem, Cart, CartItem, Order, OrderItem, OrderStatusHistory, OrderCancellation, Invoice, InvoiceItem, Coupon, CouponUsage, Promotion, PromotionBook

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'orderDate', 'status')

admin.site.register(Wishlist)
admin.site.register(WishlistItem)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OrderItem)
admin.site.register(OrderStatusHistory)
admin.site.register(OrderCancellation)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)
admin.site.register(Coupon)
admin.site.register(CouponUsage)
admin.site.register(Promotion)
admin.site.register(PromotionBook)
