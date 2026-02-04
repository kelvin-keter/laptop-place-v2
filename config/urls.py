from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views  # 1. NEW: Import for Login/Logout

# 2. UPDATED: Added 'add_staff' to the imports list
from core.views import index, product_detail, contact, about, upload_product, add_staff

urlpatterns = [
    # Admin Panel (Default Django Admin)
    path('admin/', admin.site.urls),
    
    # Homepage
    path('', index, name='index'),

    # Product Detail Page
    path('product/<int:pk>/', product_detail, name='product_detail'),

    # Contact Us Page
    path('contact/', contact, name='contact'),

    # About Us Page
    path('about/', about, name='about'),

    # STAFF PORTAL (Upload Inventory)
    path('upload/', upload_product, name='upload_product'),

    # 3. NEW: AUTHENTICATION & STAFF MANAGEMENT
    # Login Page (Uses your custom template)
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    
    # Logout (Redirects to homepage after logging out)
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    
    # Add Staff Page (Only Superusers can access this)
    path('staff/add/', add_staff, name='add_staff'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)