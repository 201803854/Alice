from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('service/', include('service.urls')),  # service 앱의 URL 패턴 포함
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)