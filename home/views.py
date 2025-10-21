from django.shortcuts import render
from .models import HeroSlide
from coffee.models import CoffeeProduct, CoffeeCategory, CoffeeBean
from restaurant.models import MenuItem, MenuCategory
from hotel.models import Room


def home(request):
    rooms = Room.objects.all().order_by("-created_at")
    featured_rooms = Room.objects.all().order_by("-created_at")

    # Fetch all menu categories and their associated items
    menu_categories = MenuCategory.objects.all().order_by('order', 'name')
    menu_data = []
    for category in menu_categories:
        items = category.items.all().order_by("-created_at")[:8]  # Limit to 8 items per category
        menu_data.append({
            'category': category,
            'items': items
        })

    hero_slides = HeroSlide.objects.filter(is_active=True).order_by("order")

    featured_coffees = (
        CoffeeProduct.objects.filter(is_available=True, stock_quantity__gt=0)
        .select_related("coffee_bean", "roast_level")
        .order_by("?")[:6]
    )

    categories = CoffeeCategory.objects.all()[:8]

    total_products = CoffeeProduct.objects.filter(is_available=True).count()
    total_beans = CoffeeBean.objects.count()
    total_categories = CoffeeCategory.objects.count()

    context = {
        "rooms": rooms,
        "featured_rooms": featured_rooms,
        "menu_data": menu_data,  # Pass the structured menu data
        "featured_coffees": featured_coffees,
        "categories": categories,
        "stats": {
            "total_products": total_products,
            "total_beans": total_beans,
            "total_categories": total_categories,
        },
        "hero_slides": hero_slides,
    }
    return render(request, "index.html", context)


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")


def privacy(request):
    return render(request, "privacy.html")


def terms(request):
    return render(request, "terms.html")


def sitemap_page(request):
    return render(request, "sitemap_page.html")
