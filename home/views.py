from django.shortcuts import render
from .models import (
    HeroSlide,
)  # Import the new model, Room, MenuItem, CoffeeProduct, CoffeeCategory, and CoffeeBean
from coffee.models import CoffeeProduct, CoffeeCategory, CoffeeBean
from restaurant.models import MenuItem
from hotel.models import Room


def home(request):
    # Base queryset - available rooms only
    rooms = Room.objects.all().order_by("-created_at")
    featured_rooms = Room.objects.all().order_by("-created_at")
    breakfast_items = MenuItem.objects.filter(category="breakfast").order_by(
        "-created_at"
    )[:8]
    coffee_items = MenuItem.objects.filter(category="coffee").order_by("-created_at")[
        :8
    ]
    american_items = MenuItem.objects.filter(category="american").order_by(
        "-created_at"
    )[:8]
    indian_items = MenuItem.objects.filter(category="indian").order_by("-created_at")[
        :8
    ]
    drinks_items = MenuItem.objects.filter(category="drinks").order_by("-created_at")[
        :8
    ]
    mexican_items = MenuItem.objects.filter(category="mexican").order_by("-created_at")[
        :8
    ]
    pizza_items = MenuItem.objects.filter(category="pizza").order_by("-created_at")[:8]
    local_food_items = MenuItem.objects.filter(category="local_food").order_by(
        "-created_at"
    )[:8]
    soup_salad_mediterranean_items = MenuItem.objects.filter(
        category="soup_salad_mediterranean"
    ).order_by("-created_at")[:8]
    dessert_items = MenuItem.objects.filter(category="dessert").order_by("-created_at")[
        :8
    ]

    # Fetch active hero slides
    hero_slides = HeroSlide.objects.filter(is_active=True).order_by("order")

    # ກາເຟຂາຍດີ (ສຸ່ມ 6 ລາຍການ)
    featured_coffees = (
        CoffeeProduct.objects.filter(is_available=True, stock_quantity__gt=0)
        .select_related("coffee_bean", "roast_level")
        .order_by("?")[:6]
    )

    # ໝວດໝູ່ທັງໝົດ
    categories = CoffeeCategory.objects.all()[:8]

    # ສະຖິຕິ
    total_products = CoffeeProduct.objects.filter(is_available=True).count()
    total_beans = CoffeeBean.objects.count()
    total_categories = CoffeeCategory.objects.count()

    context = {
        "rooms": rooms,
        "featured_rooms": featured_rooms,
        "breakfast_items": breakfast_items,
        "coffee_items": coffee_items,
        "american_items": american_items,
        "indian_items": indian_items,
        "drinks_items": drinks_items,
        "mexican_items": mexican_items,
        "pizza_items": pizza_items,
        "local_food_items": local_food_items,
        "soup_salad_mediterranean_items": soup_salad_mediterranean_items,
        "dessert_items": dessert_items,
        "featured_coffees": featured_coffees,
        "categories": categories,
        "stats": {
            "total_products": total_products,
            "total_beans": total_beans,
            "total_categories": total_categories,
        },
        "hero_slides": hero_slides,  # Add slides to context
    }
    return render(request, "index.html", context)


def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")
