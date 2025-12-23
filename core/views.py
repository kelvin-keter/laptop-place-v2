from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category  # <-- IMPORTED CATEGORY HERE

def index(request):
    # 1. Start with base rule: Only show items that are in stock
    products = Product.objects.filter(in_stock=True)
    
    # 2. Get all categories for the sidebar dropdown
    categories = Category.objects.all()

    # --- EXISTING SEARCH LOGIC ---
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(category__name__icontains=query) | 
            Q(name__icontains=query)
        )

    # --- NEW ADVANCED FILTERS ---
    
    # Filter by Category (Sidebar Dropdown)
    category_filter = request.GET.get('category')
    if category_filter:
        products = products.filter(category__name=category_filter)

    # Filter by RAM (8GB vs 16GB)
    ram_filter = request.GET.get('ram')
    if ram_filter:
        products = products.filter(ram=ram_filter)

    # Filter by Condition (New vs Refurbished)
    condition_filter = request.GET.get('condition')
    if condition_filter:
        products = products.filter(condition=condition_filter)

    # Filter by Price (Max Budget)
    max_price = request.GET.get('max_price')
    if max_price:
        try:
            products = products.filter(price__lte=max_price)
        except ValueError:
            pass # Ignore if user enters text instead of numbers

    # Filter by Touchscreen (Checkbox)
    touchscreen = request.GET.get('touchscreen')
    if touchscreen == 'on':
        products = products.filter(touchscreen=True)

    # --- CONTEXT ---
    context = {
        'products': products,
        'categories': categories,
        # Pass these back so the sidebar stays "checked" after filtering
        'selected_ram': ram_filter,
        'selected_condition': condition_filter,
        'selected_touchscreen': touchscreen,
        'selected_max_price': max_price,
        'selected_category': category_filter,
    }
    return render(request, 'core/index.html', context)

# KEEPING YOUR PERFECT PRODUCT_DETAIL VIEW
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # Logic: Same category, exclude current, top 3
    related_products = Product.objects.filter(category=product.category).exclude(pk=pk)[:3]
    
    context = {
        'product': product,
        'related_products': related_products
    }
    return render(request, 'core/product_detail.html', context)