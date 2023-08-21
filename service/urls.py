from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('convert_audio/', views.convert_audio, name='convert_audio'),
    path('mymap/', TemplateView.as_view(template_name="index.html")),
    path('temp/',TemplateView.as_view(template_name="index_final.html"))
]
