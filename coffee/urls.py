from django.urls import path
from . import views


urlpatterns = [
  
    path("", views.coffee_list_view, name="coffee_list"),
    path("<slug:slug>/", views.coffee_detail_view, name="coffee_detail"),

    path("category/<int:category_id>/", views.category_view, name="category"),
    path("category/<slug:slug>/", views.category_detail_view, name="category_detail"),
 
    path("<slug:slug>/review/", views.add_review, name="add_review"),

    path("compare/", views.compare_view, name="compare"),

    path("api/search/", views.api_coffee_search, name="api_coffee_search"),
    path("api/price-range/", views.api_price_range, name="api_price_range"),
]
