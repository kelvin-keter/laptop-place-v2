from django.shortcuts import render, get_object_or_404
from django.db.models import Q  # Needed for the search logic
from .models import Product

def index(request):
    # 1. Start with your base rule: Only show items that are in stock
    products = Product.objects.filter(in_stock=True)
    
    # 2. Check if the user clicked a category link (e.g., /?q=HP)
    query = request.GET.get('q')
    
    if query:
        # If they did, filter the list further.
        # This searches if the 'category name' OR the 'product name' contains the query.
        # 'icontains' makes it case-insensitive (so 'hp' finds 'HP').
        products = products.filter(
            Q(category__name__icontains=query) | 
            Q(name__icontains=query)
        )
    
    context = {
        'products': products
    }
    return render(request, 'core/index.html', context)

# UPDATED: This view now fetches the product AND related items
def product_detail(request, pk):
    # 'pk' is the Primary Key (ID) of the laptop
    product = get_object_or_404(Product, pk=pk)
    
    # NEW LOGIC: Get related products
    # 1. Filter by the same category
    # 2. Exclude the current product (so we don't show it to them again)
    # 3. Slice [:3] to only show the top 3 results
    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)[:3]
    
    context = {
        'product': product,
        'related_products': related_products
    }
    return render(request, 'core/product_detail.html', context)