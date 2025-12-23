from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category

def index(request):
    products = Product.objects.filter(in_stock=True)
    categories = Category.objects.all()
    featured_products = Product.objects.filter(in_stock=True, is_featured=True)[:3]

    q = request.GET.get('q')
    if q:
        products = products.filter(Q(category__name__icontains=q) | Q(name__icontains=q))

    cat = request.GET.get('category')
    if cat:
        products = products.filter(category__name=cat)

    ram = request.GET.get('ram')
    if ram:
        products = products.filter(ram=ram)

    cond = request.GET.get('condition')
    if cond:
        products = products.filter(condition=cond)

    price = request.GET.get('max_price')
    if price:
        try:
            products = products.filter(price__lte=price)
        except ValueError:
            pass

    touch = request.GET.get('touchscreen')
    if touch == 'on':
        products = products.filter(touchscreen=True)

    context = {
        'products': products,
        'featured_products': featured_products,
        'categories': categories,
        'selected_ram': ram,
        'selected_condition': cond,
        'selected_touchscreen': touch,
        'selected_max_price': price,
        'selected_category': cat,
    }
    return render(request, 'core/index.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related = Product.objects.filter(category=product.category).exclude(pk=pk)[:3]
    return render(request, 'core/product_detail.html', {'product': product, 'related_products': related})

def contact(request):
    return render(request, 'core/contact.html')

def about(request):
    return render(request, 'core/about.html')