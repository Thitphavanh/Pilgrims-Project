from django.shortcuts import render
from hotel.models import *
from coffee.models import *
from restaurant.models import MenuItem
from django.http import JsonResponse
from django.core.paginator import Paginator





def home(request):
    featured_rooms = Room.objects.filter(is_available=True)
      # Base queryset - available rooms only
    rooms = (
        Room.objects.filter(is_available=True, is_out_of_order=False)
        .select_related("room_type")
        .prefetch_related("amenities", "room_images", "roomamenity_set__amenity")
    )
    
    breakfast_items = MenuItem.objects.filter(category="breakfast").order_by("-created_at")[:8]
    coffee_items = MenuItem.objects.filter(category="coffee").order_by("-created_at")[:8]
    american_items = MenuItem.objects.filter(category="american").order_by("-created_at")[:8]
    indian_items = MenuItem.objects.filter(category="indian").order_by("-created_at")[:8]
    drinks_items = MenuItem.objects.filter(category="drinks").order_by("-created_at")[:8]
    mexican_items = MenuItem.objects.filter(category="mexican").order_by("-created_at")[:8]
    pizza_items = MenuItem.objects.filter(category="pizza").order_by("-created_at")[:8]
    local_food_items = MenuItem.objects.filter(category="local_food").order_by("-created_at")[:8]
    soup_salad_mediterranean_items = MenuItem.objects.filter(category="soup_salad_mediterranean").order_by("-created_at")[:8]
    
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
        "featured_coffees": featured_coffees,
        "categories": categories,
        "stats": {
            "total_products": total_products,
            "total_beans": total_beans,
            "total_categories": total_categories,
        },
    }
    return render(request, "index.html", context)
