from django.contrib import admin
from django.urls import path
# UPDATED: Added 'contact' to the list of imports
from core.views import index, product_detail, contact
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),
    
    # Homepage (http://laptopplacekenya.com/)
    path('', index, name='index'),

    # Product Detail Page
    path('product/<int:pk>/', product_detail, name='product_detail'),

    # NEW: Contact Us Page (http://laptopplacekenya.com/contact/)
    path('contact/', contact, name='contact'),
]

# This ensures images load correctly when you run the server locally
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)