from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('service/', include('service.urls')),  # service 앱의 URL 패턴 포함
]
