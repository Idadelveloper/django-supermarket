from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')

def product(request):
    return render(request, 'product.html')

def checkout(request):
    return render(request, 'checkout.html')