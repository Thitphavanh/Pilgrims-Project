from django.shortcuts import render, get_object_or_404
from .models import MenuItem
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import DetailView, ListView


def restaurant(request):
    test = "test"
    context = {
        "test": test,
    }
    return render(request, "restaurant/restaurant.html", context)


def menu_item(request):
    """Restaurant menu view"""
    breakfast_items = MenuItem.objects.filter(category="breakfast").order_by("-created_at")[:12]
    coffee_items = MenuItem.objects.filter(category="coffee").order_by("-created_at")[:12]
    american_items = MenuItem.objects.filter(category="american").order_by("-created_at")[:12]
    indian_items = MenuItem.objects.filter(category="indian").order_by("-created_at")[:12]
    drinks_items = MenuItem.objects.filter(category="drinks").order_by("-created_at")[:12]
    mexican_items = MenuItem.objects.filter(category="mexican").order_by("-created_at")[:12]
    pizza_items = MenuItem.objects.filter(category="pizza").order_by("-created_at")[:12]
    local_food_items = MenuItem.objects.filter(category="local_food").order_by("-created_at")[:12]
    soup_salad_mediterranean_items = MenuItem.objects.filter(
        category="soup_salad_mediterranean"
    ).order_by("-created_at")[:12]
    dessert_items = MenuItem.objects.filter(category="dessert").order_by("-created_at")[:12]

    for item in breakfast_items:
        item.price_usd = item.price / 20000 # Assuming 1 USD = 20000 LAK
    for item in coffee_items:
        item.price_usd = item.price / 20000
    for item in american_items:
        item.price_usd = item.price / 20000
    for item in indian_items:
        item.price_usd = item.price / 20000
    for item in drinks_items:
        item.price_usd = item.price / 20000
    for item in mexican_items:
        item.price_usd = item.price / 20000
    for item in pizza_items:
        item.price_usd = item.price / 20000
    for item in local_food_items:
        item.price_usd = item.price / 20000
    for item in soup_salad_mediterranean_items:
        item.price_usd = item.price / 20000
    for item in dessert_items:
        item.price_usd = item.price / 20000

    context = {
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
    }
    return render(request, "restaurant/menu.html", context)


def menu_item_detail(request, slug):
    """
    Display detailed view of a single menu item
    """
    # Get the menu item or return 404
    menu_item = get_object_or_404(MenuItem, slug=slug)

    # Get related items from the same category (excluding current item)
    related_items = MenuItem.objects.filter(category=menu_item.category).exclude(
        id=menu_item.id
    )[
        :4
    ]  # Limit to 4 related items

    # Get featured items for suggestions
    featured_items = MenuItem.objects.filter(is_featured=True).exclude(id=menu_item.id)[
        :3
    ]  # Limit to 3 featured items

    # Get category display name
    category_display = dict(MenuItem.CATEGORY_CHOICES).get(
        menu_item.category, menu_item.category
    )

    context = {
        "menu_item": menu_item,
        "related_items": related_items,
        "featured_items": featured_items,
        "category_display": category_display,
        "meta_title": f"{menu_item.name} - Our Menu",
        "meta_description": menu_item.description[:160],  # SEO description
    }

    return render(request, "restaurant/menu-detail.html", context)


def menu_by_category(request, category):
    """
    Display all menu items in a specific category
    """
    # Validate category exists in choices
    valid_categories = [choice[0] for choice in MenuItem.CATEGORY_CHOICES]
    if category not in valid_categories:
        return render(request, "restaurant/404.html", status=404)

    # Get category display name
    category_display = dict(MenuItem.CATEGORY_CHOICES).get(category, category)

    # Get all items in this category
    menu_items = MenuItem.objects.filter(category=category).order_by(
        "-is_featured", "name"
    )

    # Pagination
    paginator = Paginator(menu_items, 12)  # Show 12 items per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Get featured items from this category
    featured_items = menu_items.filter(is_featured=True)[:3]

    context = {
        "category": category,
        "category_display": category_display,
        "menu_items": page_obj,
        "featured_items": featured_items,
        "total_items": menu_items.count(),
        "categories": MenuItem.CATEGORY_CHOICES,
        "meta_title": f"{category_display} Menu",
        "meta_description": f"Explore our delicious {category_display.lower()} menu items.",
    }

    return render(request, "restaurant/category-menu.html", context)


def menu_search(request):
    """
    Search functionality for menu items
    """
    query = request.GET.get("q", "").strip()
    category_filter = request.GET.get("category", "")

    menu_items = MenuItem.objects.all()

    if query:
        # Search in name and description
        menu_items = menu_items.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    if category_filter and category_filter != "all":
        menu_items = menu_items.filter(category=category_filter)

    # Order by featured items first, then by name
    menu_items = menu_items.order_by("-is_featured", "name")

    # Pagination
    paginator = Paginator(menu_items, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "menu_items": page_obj,
        "query": query,
        "category_filter": category_filter,
        "categories": MenuItem.CATEGORY_CHOICES,
        "total_results": menu_items.count(),
        "meta_title": f"Search Results for '{query}'" if query else "Menu Search",
    }

    return render(request, "restaurant/menu-search.html", context)


def featured_menu_items(request):
    """
    Display all featured menu items
    """
    featured_items = MenuItem.objects.filter(is_featured=True).order_by(
        "category", "name"
    )

    # Group by category for better display
    items_by_category = {}
    for item in featured_items:
        category_display = dict(MenuItem.CATEGORY_CHOICES).get(
            item.category, item.category
        )
        if category_display not in items_by_category:
            items_by_category[category_display] = []
        items_by_category[category_display].append(item)

    context = {
        "featured_items": featured_items,
        "items_by_category": items_by_category,
        "total_featured": featured_items.count(),
        "meta_title": "Featured Menu Items",
        "meta_description": "Discover our chef's specially selected featured menu items.",
    }

    return render(request, "restaurant/featured-menu.html", context)


# AJAX Views for dynamic content
def get_menu_item_ajax(request, slug):
    """
    AJAX endpoint to get menu item details
    """
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        try:
            menu_item = MenuItem.objects.get(slug=slug)
            data = {
                "id": menu_item.id,
                "name": menu_item.name,
                "description": menu_item.description,
                "price": str(menu_item.price),
                "category": menu_item.get_category_display(),
                "is_featured": menu_item.is_featured,
                "image_url": menu_item.image.url if menu_item.image else None,
            }
            return JsonResponse({"success": True, "data": data})
        except MenuItem.DoesNotExist:
            return JsonResponse({"success": False, "error": "Menu item not found"})

    return JsonResponse({"success": False, "error": "Invalid request"})


def get_category_items_ajax(request, category):
    """
    AJAX endpoint to get items by category
    """
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        try:
            items = MenuItem.objects.filter(category=category).order_by(
                "-is_featured", "name"
            )
            data = []
            for item in items:
                data.append(
                    {
                        "id": item.id,
                        "name": item.name,
                        "description": item.description,
                        "price": str(item.price),
                        "is_featured": item.is_featured,
                        "image_url": item.image.url if item.image else None,
                        "slug": item.slug,
                    }
                )
            return JsonResponse({"success": True, "data": data})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request"})


class MenuItemDetailView(DetailView):
    """
    Class-based view for menu item detail
    """

    model = MenuItem
    template_name = "restaurant/menu-detail.html"
    context_object_name = "menu_item"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu_item = self.get_object()

        # Add related items
        context["related_items"] = MenuItem.objects.filter(
            category=menu_item.category
        ).exclude(id=menu_item.id)[:4]

        # Add featured items
        context["featured_items"] = MenuItem.objects.filter(is_featured=True).exclude(
            id=menu_item.id
        )[:3]

        # Add category display name
        context["category_display"] = dict(MenuItem.CATEGORY_CHOICES).get(
            menu_item.category, menu_item.category
        )

        # SEO meta tags
        context["meta_title"] = f"{menu_item.name} - Our Menu"
        context["meta_description"] = menu_item.description[:160]

        return context


class MenuByCategoryView(ListView):
    """
    Class-based view for category menu
    """

    model = MenuItem
    template_name = "restaurant/category-menu.html"
    context_object_name = "menu_items"
    paginate_by = 12

    def get_queryset(self):
        category = self.kwargs["category"]
        return MenuItem.objects.filter(category=category).order_by(
            "-is_featured", "name"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.kwargs["category"]

        context["category"] = category
        context["category_display"] = dict(MenuItem.CATEGORY_CHOICES).get(
            category, category
        )
        context["total_items"] = self.get_queryset().count()

        return context
