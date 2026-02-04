from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

# UPDATED: Added 'dashboard' to the imports list
from core.views import index, product_detail, contact, about, upload_product, add_staff, dashboard

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

    # STAFF PORTAL
    path('dashboard/', dashboard, name='dashboard'),      # <--- NEW DASHBOARD PATH
    path('upload/', upload_product, name='upload_product'),

    # AUTHENTICATION & STAFF MANAGEMENT
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('staff/add/', add_staff, name='add_staff'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)