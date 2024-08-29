from django.shortcuts import render

# Create your views heree.
def cart(request):
    return render(request, 'cart.html')

def checkout(request):
    return render(request, 'checkout.html')

def shop_detail(request):
    return render(request,'shop-detail.html')

def shop(request):
    return render(request,'shop.html')

