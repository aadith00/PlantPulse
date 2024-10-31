from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from tomatoes.models import Product
from shop.models import Order

# Create your views here.

@login_required
def dashboard(request):
    return render(request, 'ecommerce_app/dashboard.html')


@login_required
def add_product(request):
    if request.method == 'POST':
        # Code to create a new product
        pass
    return render(request, 'ecommerce_app/add_product.html')


@login_required
def update_product(request, product_id):
    product = get_object_or_404(Product, pid=product_id)
    if request.method == 'POST':
        # Code to update the product
        pass
    return render(request, 'ecommerce_app/update_product.html', {'product': product})


@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, pid=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'ecommerce_app/delete_product.html', {'product': product})


@login_required
def order_list(request):
    orders = Order.objects.all()  # Get all orders
    return render(request, 'ecommerce_app/order_list.html', {'orders': orders})


@login_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.status = request.POST['status']
        order.save()
        return redirect('order_list')
    return render(request, 'ecommerce_app/update_order_status.html', {'order': order})