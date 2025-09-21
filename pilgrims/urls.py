# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("", include("home.urls")),
#     path("coffee/", include("coffee.urls")),
#     path("hotel/", include("hotel.urls")),
#     path("menu/", include("restaurant.urls")),
# ]


# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# pilgrims/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

# URLs that don't need language prefix
urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),  # For language switching
]

# URLs with language prefix
urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("", include("home.urls")),
    path("hotel/", include("hotel.urls")),
    path("menu/", include("restaurant.urls")),
    path("coffee/", include("coffee.urls")),
    prefix_default_language=False,  # Don't add /en/ prefix for default language
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
