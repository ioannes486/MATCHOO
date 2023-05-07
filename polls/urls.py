from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path("", views.index, name='index'),
    path("detail/", views.detail, name='detail'),
    path("results/", views.results, name='results'),
    path("main", views.index, name="main"),
    path('store_detail/', views.store_detail, name='store_detail'),
]
