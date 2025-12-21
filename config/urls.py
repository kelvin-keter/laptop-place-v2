from django.contrib import admin
from django.urls import path
from core.views import index
from django.conf import settings             # New import
from django.conf.urls.static import static   # New import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
]

# This is the magic part:
# It tells Django to serve media files when running locally
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)