from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .models import Cart, CartItem
from tomatoes.models import Product, ProductReview

# Create your views heree.
def checkout(request):
    return render(request, 'checkout.html')

def shop_detail(request):
    product = Product.objects.all()

    context = {
        "products" : product,
    }

    return render(request,'shop-detail.html', context)

def product_detail(request, pid):
    product = Product.objects.get(pid=pid)

    p_image = product.p_image.all()
    context = {
        "p" : product,
        "p_image" : p_image
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
    # Ensure the user is authenticated
    if request.user.is_authenticated:
        # Get the user's cart in progress
        cart = get_object_or_404(Cart, user=request.user, status='in_progress')
        
        # Get the cart item to remove
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

        # Remove the item from the cart
        cart_item.delete()

        # Redirect back to the cart page
        return redirect('cart')  # Make sure 'cart' is the name of your cart view
    else:
        # Redirect to login page or any other action if the user is not authenticated
        return redirect('login')  # Adjust as necessary
