from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem, Order, OrderItem, Customer, Coupon, Invoice, Wishlist, WishlistItem
from catalog.models import Book
from users.models import Customer as UserCustomer # Renamed to avoid confusion if necessary

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    # Ensure customer profile exists
    customer, _ = Customer.objects.get_or_create(member=request.user)
    cart, _ = Cart.objects.get_or_create(customer=customer)
    
    quantity = int(request.POST.get('quantity', 1))
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    
    cart_item.save()
    messages.success(request, f"Added {book.title} to your cart.")
    return redirect('cart')

@login_required
def cart_view(request):
    customer, _ = Customer.objects.get_or_create(member=request.user)
    cart, _ = Cart.objects.get_or_create(customer=customer)
    items = cart.items.all()
    
    total_price = sum(item.book.price * item.quantity for item in items)
    
    return render(request, 'sales/cart.html', {'cart': cart, 'items': items, 'total_price': total_price})

@login_required
def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__customer__member=request.user)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        item.quantity = quantity
        item.save()
    else:
        item.delete()
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__customer__member=request.user)
    item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('cart')

@login_required
def checkout_view(request):
    customer, _ = Customer.objects.get_or_create(member=request.user)
    cart, _ = Cart.objects.get_or_create(customer=customer)
    items = cart.items.all()
    
    if not items:
        messages.error(request, "Your cart is empty.")
        return redirect('home')
    
    total_price = sum(item.book.price * item.quantity for item in items)
    
    coupon_code = request.GET.get('coupon')
    discount = 0
    if coupon_code:
        try:
            coupon = Coupon.objects.get(code=coupon_code)
            discount = coupon.discount_amount
            total_price = max(0, total_price - discount)
            messages.success(request, f"Coupon applied: ${discount} off")
        except Coupon.DoesNotExist:
            messages.error(request, "Invalid coupon code.")

    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        # Simple order creation logic
        order = Order.objects.create(customer=customer, status='pending')
        for item in items:
            OrderItem.objects.create(order=order, book=item.book, quantity=item.quantity)
            item.book.stock -= item.quantity
            item.book.save()
        
        # Create Invoice
        Invoice.objects.create(order=order)
        
        # Clear cart
        items.delete()
        
        messages.success(request, "Order placed successfully!")
        return render(request, 'sales/order_success.html', {'order': order})

    addresses = customer.addresses.all()
    return render(request, 'sales/checkout.html', {
        'items': items, 
        'total_price': total_price,
        'addresses': addresses,
        'discount': discount
    })

@login_required
def wishlist_view(request):
    customer, _ = Customer.objects.get_or_create(member=request.user)
    wishlist, _ = Wishlist.objects.get_or_create(customer=customer)
    items = wishlist.items.all()
    return render(request, 'sales/wishlist.html', {'items': items})

@login_required
def add_to_wishlist(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    customer, _ = Customer.objects.get_or_create(member=request.user)
    wishlist, _ = Wishlist.objects.get_or_create(customer=customer)
    
    WishlistItem.objects.get_or_create(wishlist=wishlist, book=book)
    messages.success(request, f"Added {book.title} to your wishlist.")
    return redirect('book_detail', book_id=book_id)

@login_required
def remove_from_wishlist(request, item_id):
    item = get_object_or_404(WishlistItem, id=item_id, wishlist__customer__member=request.user)
    item.delete()
    messages.success(request, "Removed from wishlist.")
    return redirect('wishlist')
