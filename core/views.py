from django.shortcuts import render, get_object_or_404  # Added get_object_or_404
from .models import Product

def index(request):
    # Fetch all products from the database
    # PRESERVED: We keep your logic to only show available items
    products = Product.objects.filter(in_stock=True)
    
    context = {
        'products': products
    }
    return render(request, 'core/index.html', context)

# NEW: This view fetches one specific product
def product_detail(request, pk):
    # 'pk' is the Primary Key (ID) of the laptop
    # get_object_or_404 tries to find it, or shows a 404 error if the ID is wrong
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'core/product_detail.html', {'product': product})