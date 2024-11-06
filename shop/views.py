from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from .models import Cart, CartItem, Order
from tomatoes.models import Product
from account.models import  Customer
from django.contrib import messages

# Create your views heree.
def shop_detail(request):
    product = Product.objects.all()

    cart_items_count = 0

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, status='in_progress').first()
        if cart:
            cart_items_count = CartItem.objects.filter(cart=cart).count()

    context = {
        "products": product,
        "cart_items_count": cart_items_count
    }

    return render(request, 'shop-detail.html', context)

def product_detail(request, pid):
    product = get_object_or_404(Product, pid=pid)

    cart_items_count = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, status='in_progress').first()
        if cart:
            cart_items_count = CartItem.objects.filter(cart=cart).count()

    p_image = product.p_image.all()
    
    context = {
        "p": product,
        "p_image": p_image,
        "cart_items_count": cart_items_count
    }
    return render(request, "product-detail.html", context)

def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('id')  # This is the pid
        product_quantity = int(request.POST.get('quant'))

        product = get_object_or_404(Product, pid=product_id)

        cart = None
        if Cart.objects.filter(user=request.user, status='in_progress').exists():
            cart = Cart.objects.get(user=request.user, status='in_progress')
        else:
            cart =  Cart.objects.create(user=request.user, status='in_progress')
    
        if CartItem.objects.filter(cart=cart, product=product).exists(): 
            cart_item = CartItem.objects.get(cart=cart, product=product )
            cart_item.quantity += product_quantity
            cart_item.price = product.price
            cart_item.save()
        else:
            CartItem.objects.create(cart=cart, product=product,quantity = product_quantity,price = product.price )

        # Get total item count
        total_items = CartItem.objects.filter(cart=cart).count()

        return JsonResponse({'status': 'success', 'totalcartitems': total_items})

    return JsonResponse({'status': 'error'}, status=400)

def cart(request):
    try:
        cart = Cart.objects.get(user=request.user, status='in_progress')
        cart_items = CartItem.objects.filter(cart=cart)
        
        # Calculate total price for each cart item
        for item in cart_items:
            item.total_price = item.quantity * item.price  # Add total_price attribute

        # Calculate overall total price
        total_price = sum(item.total_price for item in cart_items)
        
    except Cart.DoesNotExist:
        cart_items = []
        total_price = 0  # Default to 0 if no cart exists

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

def remove_from_cart(request, item_id):
    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user, status='in_progress')
        
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

        cart_item.delete()

        return redirect('cart')
    else:
        return redirect('login')
    
def checkoutpage(request):
    return render(request, 'checkout.html')

def checkout(request):
    cart_items_count = 0
    cart_items = []

    try:
        cart = Cart.objects.get(user=request.user, status='in_progress')
        cart_items = CartItem.objects.filter(cart=cart)
        total_price = sum(item.quantity * item.price for item in cart_items)
        cart_items_count = cart_items.count()
        
        # Check if customer has existing billing details
        customer = Customer.objects.filter(user=request.user).first()

        if request.method == 'POST':
            # If the customer already has address info, use it. If not, create/update their info
            if not customer:
                customer = Customer(user=request.user)

            # Update the customer's address details based on the form input
            customer.first_name = request.POST.get('first_name')
            customer.last_name = request.POST.get('last_name')
            customer.phone_number = request.POST.get('phone')
            customer.address = request.POST.get('address')
            customer.address2 = request.POST.get('address2')
            customer.city = request.POST.get('city')
            customer.state = request.POST.get('state')
            customer.country = request.POST.get('country')
            customer.zip_code = request.POST.get('zip_code')
            customer.save()

            # Store total price in session and redirect to payment
            request.session['total_price'] = float(total_price)
            return redirect('payment',cart.id)

    except Cart.DoesNotExist:
        total_price = 0

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_items_count': cart_items_count,
        'customer': customer  # Pass the customer data to prefill the form
    })

def payment(request,id):
    if request.method == 'POST':
        # Retrieve the delivery time from the form data (if needed)
        delivery_time = request.POST.get('delivery_time')
        # Get the logged-in user
        user = request.user

        cart = Cart.objects.get(user=request.user, id=id)
        cart_items = CartItem.objects.filter(cart=cart)
        total_price = sum(item.quantity * item.price for item in cart_items)

        # Retrieve customer details
        customer = Customer.objects.filter(user=user).first()

        if customer:
            # Create a new order entry
            order = Order.objects.create(
                cart=cart,
                user=user,
                state=customer.state,
                total_price=total_price,
                status="Pending",
                delivery_time=delivery_time,
            )
            cart.status='Ordered'
            cart.save()
            # Optionally add a success message
            messages.success(request, "Your order has been placed successfully!")
            return redirect('order_confirmation_user', order_id=order.order_id)
        else:
            messages.error(request, "Billing address not found. Please set up your billing address.")
            return redirect('update_address')
    else:
        return render(request, 'payment.html')

def order_confirmation(request, order_id):
    # Retrieve the order by its ID
    order = Order.objects.get(order_id=order_id)
    
    # Retrieve the cart associated with the order
    cart = order.cart
    cart_items = CartItem.objects.filter(cart=cart)
    
    # Get the logged-in user
    user = request.user
    
    # Retrieve customer details
    customer = Customer.objects.filter(user=user).first()

    # Add relevant data to the context
    context = {
        'order': order,
        'cart': cart,
        'cart_items': cart_items,
        'customer': customer,
        'total_price': order.total_price,
        'delivery_time': order.delivery_time,
    }

    return render(request, 'order_confirmation.html', context)