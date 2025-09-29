from django.urls import path
from . import views


urlpatterns = [
    path("", views.hotel, name="hotel-page"),
    path("review/", views.review, name="review-page"),
    # Main reviews page
    # Platform specific pages
    path(
        "platform/<str:platform_name>/",
        views.platform_detail,
        name="platform-detail-page",
    ),
    path(
        "platform/<str:platform_name>/redirect/",
        views.platform_redirect,
        name="platform-redirect-page",
    ),
    # API endpoints
    path("api/", views.review_api, name="review-api-page"),
    # Widgets
    path("widget/rating/", views.reviews_widget, name="reviews-widget-page"),
    # Admin utilities (staff only)
    path(
        "admin/platform/<int:platform_id>/update-stats-page/",
        views.update_platform_stats,
        name="update_platform-stats-page",
    ),
    path(
        "admin/bulk-import/", views.bulk_import_reviews, name="bulk_import-reviews-page"
    ),
    # Room detail and booking
    path("room/<slug:slug>/", views.room_detail_view, name="room-detail-page"),
    # Room listings
    path("rooms/", views.rooms_list_view, name="rooms-list-page"),
    path("room/<slug:slug>/book/", views.room_booking_view, name="room-booking-page"),
    # Check-in/out functionality
    path("room/<slug:slug>/check-in/", views.room_check_in_view, name="room-check-in"),
    path("room/<slug:slug>/check-out/", views.room_check_out_view, name="room-check-out"),
    path("rooms/featured/", views.featured_rooms_view, name="featured-rooms-page"),
    path(
        "api/room-availability/",
        views.room_availability_api,
        name="room-availability-api-page",
    ),
]
