from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from restaurant.models import MenuItem, MenuCategory
from hotel.models import Room, RoomType
from coffee.models import CoffeeProduct


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages"""
    priority = 1.0
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return [
            'home-page',
            'about-page',
            'contact-page',
            'rooms-list-page',
            'menu-page',
            'coffee_list',
            'review-page',
            'privacy-page',
            'terms-page',
            'sitemap-page',
        ]

    def location(self, item):
        return reverse(item)


class MenuItemSitemap(Sitemap):
    """Sitemap for menu items"""
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return MenuItem.objects.filter(slug__isnull=False)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('menu-item-detail-page', kwargs={'slug': obj.slug})


class MenuCategorySitemap(Sitemap):
    """Sitemap for menu categories"""
    changefreq = "weekly"
    priority = 0.7
    protocol = 'https'

    def items(self):
        return MenuCategory.objects.filter(slug__isnull=False)

    def location(self, obj):
        return reverse('menu-by-category-page', kwargs={'category': obj.slug})


class RoomSitemap(Sitemap):
    """Sitemap for hotel rooms"""
    changefreq = "monthly"
    priority = 0.9
    protocol = 'https'

    def items(self):
        return Room.objects.filter(slug__isnull=False, is_out_of_order=False)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('room-detail-page', kwargs={'slug': obj.slug})


class CoffeeSitemap(Sitemap):
    """Sitemap for coffee products"""
    changefreq = "weekly"
    priority = 0.7
    protocol = 'https'

    def items(self):
        try:
            return CoffeeProduct.objects.filter(slug__isnull=False)
        except:
            return []

    def lastmod(self, obj):
        try:
            return obj.updated_at
        except:
            return None

    def location(self, obj):
        try:
            return reverse('coffee_detail', kwargs={'slug': obj.slug})
        except:
            return None


# Sitemap dictionary
sitemaps = {
    'static': StaticViewSitemap,
    'menu_items': MenuItemSitemap,
    'menu_categories': MenuCategorySitemap,
    'rooms': RoomSitemap,
    'coffee': CoffeeSitemap,
}
