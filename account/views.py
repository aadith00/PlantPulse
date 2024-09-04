from django.shortcuts import render

# Create your views here.
def account(request):
    return render(request, 'my-account.html')

def wishlist(request):
    return render(request, 'wishlist.html')

def auth(request):
    return render(request, 'autho.html' )