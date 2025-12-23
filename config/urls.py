from django.contrib import admin
from django.urls import path
# UPDATED: Added 'about' to imports
from core.views import index, product_detail, contact, about
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),
    
    # Homepage
    path('', index, name='index'),

    # Product Detail Page
    path('product/<int:pk>/', product_detail, name='product_detail'),

    # Contact Us Page
    path('contact/', contact, name='contact'),

    # NEW: About Us Page
    path('about/', about, name='about'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)