from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
# UPDATED IMPORTS: Added ProductImage
from .models import Product, Category, ProductImage
from .forms import ProductUploadForm

def index(request):
    products = Product.objects.filter(in_stock=True)
    categories = Category.objects.all()
    # Featured: Get top 4 for the 4-column layout
    featured_products = Product.objects.filter(in_stock=True, is_featured=True)[:4]

    # --- 1. SEARCH ---
    q = request.GET.get('q')
    if q:
        products = products.filter(
            Q(category__name__icontains=q) | 
            Q(name__icontains=q) |
            Q(description__icontains=q)
        )

    # --- 2. FILTERS ---
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
            products = products.filter(price__lte=int(price))
        except ValueError:
            pass

    touch = request.GET.get('touchscreen')
    if touch == 'on':
        products = products.filter(touchscreen=True)

    # --- 3. NEW FILTERS ---
    usage = request.GET.get('usage')
    if usage:
        products = products.filter(usage=usage)

    l_type = request.GET.get('type')
    if l_type:
        products = products.filter(laptop_type=l_type)

    context = {
        'products': products,
        'featured_products': featured_products,
        'categories': categories,
        'selected_ram': ram,
        'selected_condition': cond,
        'selected_touchscreen': touch,
        'selected_max_price': price,
        'selected_category': cat,
        'selected_usage': usage,
        'selected_type': l_type,
    }
    return render(request, 'core/index.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    # Related: same category, excluding current one
    related = Product.objects.filter(category=product.category).exclude(pk=pk)[:3]
    return render(request, 'core/product_detail.html', {'product': product, 'related_products': related})

def contact(request):
    return render(request, 'core/contact.html')

def about(request):
    return render(request, 'core/about.html')

# --- STAFF UPLOAD VIEW (UPDATED FOR GALLERY) ---
@user_passes_test(lambda u: u.is_staff, login_url='/admin/login/')
def upload_product(request):
    if request.method == 'POST':
        form = ProductUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            # 1. Save the main product first
            product = form.save()
            
            # 2. Handle the Multiple Gallery Images
            # We look for the field 'gallery_images' which we defined in forms.py
            gallery_files = request.FILES.getlist('gallery_images')
            
            for f in gallery_files:
                # Create a new ProductImage entry for each file
                ProductImage.objects.create(product=product, image=f)
            
            # Success Message
            msg = f'✅ SUCCESS: "{product.name}" uploaded successfully!'
            if gallery_files:
                msg += f' (Added {len(gallery_files)} gallery photos)'
            
            messages.success(request, msg)
            return redirect('upload_product')
        else:
            # ERROR HANDLING: If form is invalid, show an error message
            messages.error(request, '❌ Upload Failed. Please check the form for errors below.')
            
    else:
        form = ProductUploadForm()
    
    return render(request, 'core/upload_product.html', {'form': form})