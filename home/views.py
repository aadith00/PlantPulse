from django.shortcuts import render
from tomatoes.models import Variety, Product, Disease
from shop.models import CartItem, Cart
# Create your views here.

def index(request):
    product = Product.objects.all()
    variety = Variety.objects.all()
    disease = Disease.objects.all()

    cart_items_count = 0

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, status='in_progress').first()
        if cart:
            cart_items_count = CartItem.objects.filter(cart=cart).count()

    context = {
        "products": product,
        "varieties": variety,
        "diseases": disease,
        "cart_items_count": cart_items_count
    }

    return render(request, 'index.html', context)

def about(request):
    cart_items_count = 0

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, status='in_progress').first()
        if cart:
            cart_items_count = CartItem.objects.filter(cart=cart).count()

    context = {
        "cart_items_count": cart_items_count
    }

    return render(request, 'about.html', context)

def contact(request):
    cart_items_count = 0

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, status='in_progress').first()
        if cart:
            cart_items_count = CartItem.objects.filter(cart=cart).count()

    context = {
        "cart_items_count": cart_items_count
    }
    
    return render(request, 'contact-us.html', context)

def gallery(request):
    cart_items_count = 0

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, status='in_progress').first()
        if cart:
            cart_items_count = CartItem.objects.filter(cart=cart).count()

    context = {
        "cart_items_count": cart_items_count
    }

    return render(request, 'gallery.html', context)