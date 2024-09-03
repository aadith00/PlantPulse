from django.shortcuts import render

# Create your views here.
def modpage(request):
    return render(request, 'model.html')