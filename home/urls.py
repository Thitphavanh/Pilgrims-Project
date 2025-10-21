from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home-page"),
    path("about/", views.about, name="about-page"),
    path("contact/", views.contact, name="contact-page"),
    path("privacy/", views.privacy, name="privacy-page"),
    path("terms/", views.terms, name="terms-page"),
    path("sitemap/", views.sitemap_page, name="sitemap-page"),
]
