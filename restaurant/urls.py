from django.urls import path
from . import views


urlpatterns = [
    path("", views.menu_item, name="menu-page"),
    path("<slug:slug>/", views.menu_item_detail, name="menu-item-detail-page"),
    path(
        "category/<str:category>/", views.menu_by_category, name="menu-by-category-page"
    ),
    # Featured items page
    path("featured/", views.featured_menu_items, name="featured-menu-page"),
    # Search functionality
    path("search/", views.menu_search, name="menu-search-page"),
    # AJAX endpoints
    path(
        "ajax/menu-item/<slug:slug>/",
        views.get_menu_item_ajax,
        name="get_menu_item_ajax",
    ),
    path(
        "ajax/category/<str:category>/",
        views.get_category_items_ajax,
        name="get_category_items_ajax",
    ),
]
