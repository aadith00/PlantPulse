from django.shortcuts import render
from tomatoes.models import Variety, Product, Disease
# Create your views here.

def index(request):
    product = Product.objects.all()
    variety = Variety.objects.all()
    disease = Disease.objects.all()

    context = {
        "products" : product,
        "varieties" : variety,
        "diseases" : disease
    }
    
    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact-us.html')

def gallery(request):
    return render(request, 'gallery.html')