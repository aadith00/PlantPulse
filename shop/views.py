from django.shortcuts import render
from tomatoes.models import Product

# Create your views heree.
def cart(request):
    return render(request, 'cart.html')

def checkout(request):
    return render(request, 'checkout.html')

def shop_detail(request):
    return render(request,'shop-detail.html')

def shop(request):
    return render(request,'shop.html')

def product_detail(request, pid):
    product = Product.objects.get(pid=pid)

    p_image = product.p_image.all()

    context = {
        "p" : product
    }



    return render(request, "product-detail.html", context)

