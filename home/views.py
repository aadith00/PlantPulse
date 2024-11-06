from django.shortcuts import redirect, render
from tomatoes.models import Vegetables, Product, Disease
from shop.models import CartItem, Cart, ContactUs
from django.contrib import messages

# Create your views here.

def index(request):
    product = Product.objects.all()
    vegetables = Vegetables.objects.all()
    disease = Disease.objects.all()

    cart_items_count = 0

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user, status='in_progress').first()
        if cart:
            cart_items_count = CartItem.objects.filter(cart=cart).count()

    context = {
        "products": product,
        "vegetables": vegetables,
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
    if request.method == 'POST':
        # Retrieve the delivery time from the form data (if needed)
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        contact=ContactUs.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )
        contact.save()

        messages.success(request, "Your Message has been sented successfully!")
        return redirect('contact',)
    
    else:
        return render(request, 'contact-us.html')

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