
from django.urls import path
from . import views

urlpatterns = [
    path('', views.gallery_category_list, name='gallery_category_list'),
    path('<slug:category_slug>/', views.gallery_image_list, name='gallery_image_list'),
]
