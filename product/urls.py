from django.urls import path
from . import views

urlpatterns = [
    # Using Class-Based Views
    path("", views.ProductListView.as_view(), name="product_list"),
    path("category/<slug:category_slug>/", views.ProductListView.as_view(), name="product_list_by_category"),
    path("<slug:slug>/", views.ProductDetailView.as_view(), name="product_detail"),

    # Uncomment below to use Function-Based Views instead
    # path("", views.product_list, name="product_list"),
    # path("category/<slug:category_slug>/", views.product_list, name="product_list_by_category"),
    # path("<slug:slug>/", views.product_detail, name="product_detail"),
]
