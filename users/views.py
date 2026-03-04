from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Member, Customer, Address

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # In this custom implementation, we use email as the username for authentication
        # since the entity table specified email but we inherit from AbstractUser
        try:
            member = Member.objects.get(email=email)
            user = authenticate(request, username=member.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('home')
            else:
                messages.error(request, "Invalid email or password.")
        except Member.DoesNotExist:
            messages.error(request, "Invalid email or password.")
            
    return render(request, 'users/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        dob = request.POST.get('dob')
        
        if Member.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        elif Member.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        else:
            user = Member.objects.create_user(
                username=username, 
                email=email, 
                password=password,
                dob=dob if dob else None,
                role='customer'
            )
            # Create Customer profile
            Customer.objects.create(member=user)
            
            login(request, user)
            messages.success(request, f"Welcome to Antigravity Bookstore, {user.username}!")
            return redirect('home')
            
    return render(request, 'users/register.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')

@login_required
def profile_view(request):
    customer, _ = Customer.objects.get_or_create(member=request.user)
    addresses = customer.addresses.all()
    # Fetch orders from the sales app
    from sales.models import Order
    orders = Order.objects.filter(customer=customer).order_by('-orderDate')
    
    context = {
        'addresses': addresses,
        'orders': orders,
    }
    return render(request, 'users/profile.html', context)

@login_required
def add_address_view(request):
    if request.method == 'POST':
        customer, _ = Customer.objects.get_or_create(member=request.user)
        num = request.POST.get('num')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        is_default = request.POST.get('is_default') == 'on'
        
        if is_default:
            customer.addresses.update(is_default=False)
            
        Address.objects.create(
            customer=customer,
            num=num,
            street=street,
            city=city,
            state=state,
            is_default=is_default
        )
        messages.success(request, "Address added successfully!")
    return redirect('profile')
