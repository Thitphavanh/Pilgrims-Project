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


# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import TemplateView
from .sitemaps import sitemaps

# URLs that don't need language prefix
urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),  # For language switching
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name='robots'),
]

# URLs with language prefix
urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("", include("home.urls")),
    path("hotel/", include("hotel.urls")),
    path("menu/", include("restaurant.urls")),
    path("coffee/", include("coffee.urls")),
    path("gallery/", include("gallery.urls")),
    prefix_default_language=False,  # Don't add /lo/ prefix for default language (Lao)
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
