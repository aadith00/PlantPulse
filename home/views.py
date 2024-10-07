from django.shortcuts import render
from tomatoes.models import Variety, Product
# Create your views here.

def index(request):
    product = Product.objects.all()

    context = {
        "products" : product
    }
    
    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact-us.html')

def gallery(request):
    return render(request, 'gallery.html')