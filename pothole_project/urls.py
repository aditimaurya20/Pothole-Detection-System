from django.contrib import admin
from django.urls import path, include   # ✅ THIS FIXES ERROR
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),   # optional but recommended
    path('', include('detector.urls')),
]

# ✅ for media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)