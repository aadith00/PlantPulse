from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .models import Cart, CartItem, Order
from tomatoes.models import Product
from account.models import BillingAddress
from django.contrib import messages

# Create your views heree.
def checkoutpage(request):
    return render(request, 'checkout.html')

from django.shortcuts import render, redirect

def payment(request):
    if request.method == 'POST':
        # Capture the preferred delivery time
        preferred_delivery_time = request.POST.get('delivery_time')
        return redirect('order_confirmation')

    # If GET request, render the payment page
    return render(request, 'payment.html')


def order_confirmation(request):
    return render(request, 'order_confirmation.html')


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

def checkout(request):
    cart_items_count = 0  # Initialize cart items count
    cart_items = []

    try:
        cart = Cart.objects.get(user=request.user, status='in_progress')
        cart_items = CartItem.objects.filter(cart=cart)
        total_price = sum(item.quantity * item.price for item in cart_items)
        cart_items_count = cart_items.count()  # Get the count of items in the cart

        if request.method == 'POST':
            BillingAddress.objects.create(
                user=request.user,
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                address=request.POST.get('address'),
                address2=request.POST.get('address2'),
                city=request.POST.get('city'),
                state=request.POST.get('state'),
                country=request.POST.get('country'),
                zip_code=request.POST.get('zip_code'),
                phone=request.POST.get('phone'),
            )
            return redirect('payment')

    except Cart.DoesNotExist:
        total_price = 0  # Set to zero if there is no cart

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_items_count': cart_items_count  # Pass the cart items count to the template
    })

def place_order(request):
    cart = get_object_or_404(Cart, user=request.user, status='in_progress')
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        return redirect('shop')  # Redirect to shop if there are no items in the cart

    if request.method == 'POST':
        # Get the data from the request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        zip_code = request.POST.get('zip_code')

        # Validate required fields
        if not all([first_name, last_name, address, city, state, country, zip_code]):
            messages.error(request, "Please enter the required details.")
            return render(request, 'place_order.html', {
                'cart_items': cart_items,
                'total_price': sum(item.quantity * item.price for item in cart_items)
            })

        # Save the billing address
        billing_address = BillingAddress.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            address=address,
            address2=request.POST.get('address2'),  # Optional
            city=city,
            state=state,
            country=country,
            zip_code=zip_code,
            phone=request.POST.get('phone'),  # Optional
        )

        # Create the order
        order = Order.objects.create(
            user=request.user,
            billing_address=billing_address,
            total_price=sum(item.quantity * item.price for item in cart_items)
        )

        # Link cart items to the order and clear the cart
        for item in cart_items:
            item.order = order
            item.save()

        # Clear the cart
        cart.items.clear()

        return redirect('order_confirmation')  # Redirect to confirmation page

    return render(request, 'place_order.html', {
        'cart_items': cart_items,
        'total_price': sum(item.quantity * item.price for item in cart_items)
    })