from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.shortcuts import redirect
from account.models import Farmer, Customer
from tomatoes.models import Product
from shop.models import Order, ContactUs
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.urls import reverse

@login_required
def dashboard(request):
    user_count = User.objects.count()  # Fetch the user count
    order_count = Order.objects.count()  # Fetch the total orders count
    total_sales = Order.objects.aggregate(total=Sum('total_price'))['total'] or 0  # Calculate total sales
    
    context = {
        'user_count': user_count,  # Pass the user count to the template
        'order_count': order_count,  # Pass the order count to the template
        'total_sales': total_sales,  # Pass the total sales to the template
    }
    
    return render(request, 'dashboard.html', context)

def admin_logout(request):
    logout(request)
    return redirect('login')  # Redirect to your login page after logout

def manage_users(request):
    users = User.objects.all()
    user_roles = []

    for user in users:
        if hasattr(user, 'farmer'):
            role = 'Farmer'
        elif hasattr(user, 'customer'):
            role = 'Customer'
        else:
            role = 'Admin'
        user_roles.append((user, role))

    return render(request, 'manage_users.html', {'user_roles': user_roles, 'users' : users})

from django.http import JsonResponse

def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'GET':
        # Determine the user's role
        if Farmer.objects.filter(user=user).exists():
            role = 'farmer'
        elif Customer.objects.filter(user=user).exists():
            role = 'customer'
        else:
            role = 'admin'  # Assign admin if the user is not in both tables

        context = {
            'user': user,
            'role': role,
        }
        return render(request, 'edit_user_modal.html', context)

    elif request.method == 'POST':
        # Handle the form submission to update the user
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()
        
        return JsonResponse({'success': True})

def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        
        # Register into the appropriate table
        if role == 'farmer':
            Farmer.objects.create(user=user)
            messages.success(request, 'Farmer registered successfully!')
        elif role == 'customer':
            Customer.objects.create(user=user)
            messages.success(request, 'Customer registered successfully!')
        
        return redirect('manage_users')  # Redirect back to the manage users page

def order_confirmation(request):
    return render(request, 'order_confirmation.html')

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        user.delete()
        return redirect('manage_users')
    return render(request, 'confirm_delete.html', {'user': user})

@login_required
def manage_orders(request):
    # Apply filters if provided in the request
    order_id = request.GET.get('order_id')
    status = request.GET.get('status')

    # Query the orders based on filters
    orders = Order.objects.all()
    if order_id:
        orders = orders.filter(id=order_id)
    if status:
        orders = orders.filter(status=status)

    # Summary for the overview section
    total_orders = orders.count()
    pending_orders = orders.filter(status='Pending').count()
    completed_orders = orders.filter(status='Completed').count()

    context = {
        'orders': orders,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
    }
    return render(request, 'order_list.html', context)

def view_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Collect order details, including items in the order
    order_details = {
        'order_id': order.order_id,
        'customer_name': order.user.username,
        'status': order.status,
        'date': order.created_at.strftime('%b %d, %Y'),
        'total': float(order.total_price),
        'items': [
            {
                'product_title': item.product.title,
                'quantity': item.quantity,
                'price': float(item.price),
                'subtotal': float(item.quantity * item.price)
            }
            for item in order.cart.items.all()  # Access related cart items
        ]
    }

    # Return order details as JSON for display in modal
    return JsonResponse(order_details)

@require_POST
def delete_order(request, order_id):
    print("hello")
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return JsonResponse({'message': 'Order deleted successfully'})

def manage_products(request):
    products = Product.objects.all()  # Fetch all products from the database
    return render(request, 'manage_prod.html', {'products': products})

def view_messages(request):
    messages = ContactUs.objects.all()
    return render(request, 'user_messages.html', {'messages': messages})