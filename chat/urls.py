from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.home, name='home'),
    path('generate_text/', views.generate_text, name='generate_text'),
]
