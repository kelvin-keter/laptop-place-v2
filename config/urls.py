from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# UPDATED: Added 'upload_product' to the imports list
from core.views import index, product_detail, contact, about, upload_product

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),
    
    # Homepage
    path('', index, name='index'),

    # Product Detail Page
    path('product/<int:pk>/', product_detail, name='product_detail'),

    # Contact Us Page
    path('contact/', contact, name='contact'),

    # About Us Page
    path('about/', about, name='about'),

    # NEW: Staff Upload Portal
    # This connects the URL "yourwebsite.com/upload" to the view we just made
    path('upload/', upload_product, name='upload_product'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)