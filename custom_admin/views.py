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
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import TruncDate
from django.db.models import Count

@login_required
def dashboard(request):
    # Fetch the user count
    user_count = User.objects.count()
    total_saless = Order.objects.aggregate(total=Sum('total_price'))['total'] or 0
    # Fetch the total orders count
    order_count = Order.objects.count()

    # Calculate total sales
    total_sales = (
    Order.objects.annotate(date=TruncDate('created_at'))
    .values('date')
    .annotate(total=Sum('total_price'))
    .order_by('date')
)

    # Get data for the last 4 weeks
    today = timezone.now()
    last_4_weeks = [today - timedelta(weeks=i) for i in range(4)]

    # Get new users for the last 4 weeks
    user_growth_data = []
    user_growth_labels = []
    for week_start in last_4_weeks[::-1]:  # Reverse to display the most recent week first
        week_end = week_start + timedelta(weeks=1)
        new_users_count = User.objects.filter(date_joined__gte=week_start, date_joined__lt=week_end).count()
        user_growth_data.append(new_users_count)
        user_growth_labels.append(f'Week {len(user_growth_labels) + 1}')

    recent_orders = Order.objects.all()
    daily_user_count = (
    User.objects.annotate(date=TruncDate('date_joined'))
    .values('date')
    .annotate(count=Count('id'))
    .order_by('date')
)

    # Pass the data to the template
    context = {
        'recent_orders': recent_orders,
        'user_count': user_count,
        'order_count': order_count,
        'total_sales': total_sales,
        'total_saless': total_saless,
        'user_growth_labels': user_growth_labels,  # Pass labels (e.g., 'Week 1', 'Week 2', ...)
        'new_user_data': user_growth_data, 
         'daily_user_count':daily_user_count, # Pass new user data for the weeks
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

def view_recent_orders(request):
    # Fetch all orders and slice the last 3
    recent_orders = Order.objects.order_by('-created_at')[:3]
    
    # Pass the orders to the template
    return render(request, 'dashboard.html', {'recent_orders': recent_orders})

def update_order_status(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get("status")
        
        if new_status in ["Pending", "Completed", "Cancelled"]:
            order.status = new_status
            order.save()
            messages.success(request, f"Order #{order.id} status updated to {new_status}.")
        else:
            messages.error(request, "Invalid status selected.")

    return redirect("manage_orders")  # Redirect to the orders management page

def cancel_order(request, order_id):
    # Get the order instance
    order = get_object_or_404(Order, order_id=order_id)

    # Ensure the order is in 'Pending' status before allowing cancellation
    if order.status == "Pending":
        # Update the status to 'Cancelled'
        order.status = "Cancelled"
        order.save()

        # Redirect to the order history page or some confirmation page
        return redirect('my-account')  # Redirect back to the order history page

    # If the order status is not 'Pending', you can show an error or just redirect back
    return redirect('my-account')  # Redirect back with an error message if necessary