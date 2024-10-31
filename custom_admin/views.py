from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from tomatoes.models import Product
from shop.models import Order

@login_required
def dashboard(request):
    if request.user.is_superuser:
        return render(request, 'dashboard.html')
    else:
        return redirect('index') 

@login_required
def add_product(request):
    if request.method == 'POST':
        # Code to create a new product
        pass
    return render(request, 'add_product.html')

@login_required
def update_product(request, product_id):
    product = get_object_or_404(Product, pid=product_id)
    if request.method == 'POST':
        # Code to update the product
        pass
    return render(request, 'custom_admin/update_product.html', {'product': product})


@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, pid=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'custom_admin/delete_product.html', {'product': product})


@login_required
def order_list(request):
    orders = Order.objects.all()  # Get all orders
    return render(request, 'custom_admin/order_list.html', {'orders': orders})


@login_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.status = request.POST['status']
        order.save()
        return redirect('order_list')
    return render(request, 'custom_admin/update_order_status.html', {'order': order})
