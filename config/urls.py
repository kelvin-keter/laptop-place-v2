from django.contrib import admin
from django.urls import path
# We import views from the 'core' app folder
from core.views import index, product_detail
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),
    
    # Homepage (http://your-site.com/)
    path('', index, name='index'),

    # Product Detail Page (http://your-site.com/product/1/)
    # <int:pk> means "expect a number here" (like an ID)
    path('product/<int:pk>/', product_detail, name='product_detail'),
]

# This ensures images load correctly when you run the server locally
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)