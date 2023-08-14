from django.urls import path
from . import views

from django.views.generic import TemplateView

urlpatterns = [
    path('convert_audio/', views.convert_audio, name='convert_audio'),
    path('stt/', TemplateView.as_view(template_name="indexes.html")),

]
