from django.shortcuts import render
from .models import Product

def index(request):
    # Fetch all products from the database
    products = Product.objects.filter(in_stock=True)
    
    context = {
        'products': products
    }
    return render(request, 'core/index.html', context)