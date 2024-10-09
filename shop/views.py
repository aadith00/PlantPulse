from django.shortcuts import render
from tomatoes.models import Product, ProductReview

# Create your views heree.
def cart(request):
    return render(request, 'cart.html')

def checkout(request):
    return render(request, 'checkout.html')

def shop_detail(request):
    product = Product.objects.all()

    context = {
        "products" : product,
    }

    return render(request,'shop-detail.html', context)

def shop(request):
    return render(request,'shop.html')

def product_detail(request, pid):
    product = Product.objects.get(pid=pid)

    p_image = product.p_image.all()
    context = {
        "p" : product,
        "p_image" : p_image
    }

    return render(request, "product-detail.html", context)

