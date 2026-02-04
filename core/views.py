from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
# NEW IMPORT: Required for creating users
from django.contrib.auth.forms import UserCreationForm

from .models import Product, Category, ProductImage
from .forms import ProductUploadForm

def index(request):
    products = Product.objects.filter(in_stock=True)
    categories = Category.objects.all()
    
    # --- FEATURED SECTION FIX ---
    # We order by '-created_at' (Newest First) before slicing [:4].
    featured_products = Product.objects.filter(in_stock=True, is_featured=True).order_by('-created_at')[:4]

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
    related = Product.objects.filter(category=product.category).exclude(pk=pk)[:3]
    return render(request, 'core/product_detail.html', {'product': product, 'related_products': related})

def contact(request):
    return render(request, 'core/contact.html')

def about(request):
    return render(request, 'core/about.html')

# --- STAFF UPLOAD VIEW ---
@user_passes_test(lambda u: u.is_staff, login_url='/login/')
def upload_product(request):
    if request.method == 'POST':
        form = ProductUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            # 1. Save the main product first
            product = form.save()
            
            # 2. Handle the Multiple Gallery Images
            gallery_files = request.FILES.getlist('gallery_images')
            
            for f in gallery_files:
                ProductImage.objects.create(product=product, image=f)
            
            # Success Message
            msg = f'✅ SUCCESS: "{product.name}" uploaded successfully!'
            if gallery_files:
                msg += f' (Added {len(gallery_files)} gallery photos)'
            
            messages.success(request, msg)
            return redirect('upload_product')
        else:
            # ERROR HANDLING
            messages.error(request, '❌ Upload Failed. Please check the form for errors below.')
            
    else:
        form = ProductUploadForm()
    
    return render(request, 'core/upload_product.html', {'form': form})

# --- NEW: ADD STAFF VIEW (Superuser Only) ---
@user_passes_test(lambda u: u.is_superuser, login_url='/login/')
def add_staff(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically make them "Staff" so they can access the upload page
            user.is_staff = True
            user.save()
            messages.success(request, f'✅ Staff account created for {user.username}!')
            return redirect('add_staff')
    else:
        form = UserCreationForm()
    
    return render(request, 'core/add_staff.html', {'form': form})