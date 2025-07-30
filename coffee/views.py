from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count, Min, Max
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from .models import CoffeeProduct, CoffeeBean, RoastLevel, CoffeeCategory, CoffeeReview


def home_view(request):
    """ໜ້າຫຼັກ - ສະແດງກາເຟແນະນຳແລະໝວດໝູ່"""

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
        "featured_coffees": featured_coffees,
        "categories": categories,
        "stats": {
            "total_products": total_products,
            "total_beans": total_beans,
            "total_categories": total_categories,
        },
    }

    return render(request, "coffee/home.html", context)


# def coffee_list_view(request):
#     """ໜ້າລາຍການກາເຟທັງໝົດ"""

#     # ຕົວກອງ
#     category = request.GET.get("category")
#     roast_level = request.GET.get("roast")
#     bean_type = request.GET.get("bean")
#     grind_type = request.GET.get("grind")
#     min_price = request.GET.get("min_price")
#     max_price = request.GET.get("max_price")
#     search = request.GET.get("search")
#     sort_by = request.GET.get("sort", "name")

#     # Query ພື້ນຖານ with annotations for ratings
#     coffees = (
#         CoffeeProduct.objects.filter(is_available=True)
#         .select_related("coffee_bean", "roast_level")
#         .prefetch_related("categories", "reviews")
#         .annotate(avg_rating=Avg("reviews__rating"), review_count=Count("reviews"))
#     )

#     # ໃຊ້ຕົວກອງ
#     if category:
#         coffees = coffees.filter(categories__id=category)

#     if roast_level:
#         coffees = coffees.filter(roast_level__id=roast_level)

#     if bean_type:
#         coffees = coffees.filter(coffee_bean__origin=bean_type)

#     if grind_type:
#         coffees = coffees.filter(grind_type=grind_type)

#     if min_price:
#         try:
#             coffees = coffees.filter(price__gte=float(min_price))
#         except ValueError:
#             pass

#     if max_price:
#         try:
#             coffees = coffees.filter(price__lte=float(max_price))
#         except ValueError:
#             pass

#     if search:
#         coffees = coffees.filter(
#             Q(name__icontains=search)
#             | Q(coffee_bean__name__icontains=search)
#             | Q(description__icontains=search)
#             | Q(coffee_bean__flavor_notes__icontains=search)
#         )

#     # ການເລຽງລຳດັບ
#     sort_options = {
#         "name": "name",
#         "price_low": "price",
#         "price_high": "-price",
#         "newest": "-created_at",
#         "rating": "-avg_rating",
#     }

#     if sort_by in sort_options:
#         if sort_by == "rating":
#             # Order by average rating, then by review count for ties
#             coffees = coffees.order_by("-avg_rating", "-review_count")
#         else:
#             coffees = coffees.order_by(sort_options[sort_by])

#     # Pagination
#     paginator = Paginator(coffees, 12)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     # ຂໍ້ມູນສຳລັບຕົວກອງ
#     categories = CoffeeCategory.objects.all().order_by("name")
#     roast_levels = RoastLevel.objects.all()
#     bean_types = CoffeeBean.ORIGIN_CHOICES
#     grind_types = CoffeeProduct.GRIND_CHOICES

#     # ຊ່ວງລາຄາ (optional - you can uncomment if you want to show price range)
#     # price_range = CoffeeProduct.objects.filter(is_available=True).aggregate(
#     #     min_price=Min("price"), max_price=Max("price")
#     # )

#     context = {
#         "page_obj": page_obj,
#         "categories": categories,
#         "roast_levels": roast_levels,
#         "bean_types": bean_types,
#         "grind_types": grind_types,
#         # "price_range": price_range,
#         "current_filters": {
#             "category": category,
#             "roast": roast_level,
#             "bean": bean_type,
#             "grind": grind_type,
#             "min_price": min_price,
#             "max_price": max_price,
#             "search": search,
#             "sort": sort_by,
#         },
#     }

#     return render(request, "coffee/coffee-list.html", context)


def coffee_list_view(request):
    """ໜ້າລາຍການກາເຟທັງໝົດ"""

    # Get filter parameters
    category = request.GET.get("category")
    roast_level = request.GET.get("roast")
    bean_type = request.GET.get("bean")
    grind_type = request.GET.get("grind")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    search = request.GET.get("search")
    sort_by = request.GET.get("sort", "name")

    # Base query with annotations
    coffees = (
        CoffeeProduct.objects.filter(is_available=True)
        .select_related("coffee_bean", "roast_level")
        .prefetch_related("categories", "reviews")
        .annotate(avg_rating=Avg("reviews__rating"), review_count=Count("reviews"))
    )

    initial_count = coffees.count()
    print(f"Initial product count: {initial_count}")

    # Apply filters one by one with debug info
    if category:
        try:
            category_id = int(category)
            coffees = coffees.filter(categories__id=category_id)
            print(f"After category filter ({category_id}): {coffees.count()} products")
        except (ValueError, TypeError):
            print(f"Invalid category ID: {category}")

    if roast_level:
        try:
            roast_id = int(roast_level)
            coffees = coffees.filter(roast_level__id=roast_id)
            print(f"After roast filter ({roast_id}): {coffees.count()} products")
        except (ValueError, TypeError):
            print(f"Invalid roast level ID: {roast_level}")

    if bean_type:
        coffees = coffees.filter(coffee_bean__origin=bean_type)
        print(f"After bean type filter ({bean_type}): {coffees.count()} products")

    if grind_type:
        coffees = coffees.filter(grind_type=grind_type)
        print(f"After grind type filter ({grind_type}): {coffees.count()} products")

    if min_price:
        try:
            min_price_val = float(min_price)
            coffees = coffees.filter(price__gte=min_price_val)
            print(
                f"After min price filter ({min_price_val}): {coffees.count()} products"
            )
        except (ValueError, TypeError):
            print(f"Invalid min price: {min_price}")

    if max_price:
        try:
            max_price_val = float(max_price)
            coffees = coffees.filter(price__lte=max_price_val)
            print(
                f"After max price filter ({max_price_val}): {coffees.count()} products"
            )
        except (ValueError, TypeError):
            print(f"Invalid max price: {max_price}")

    if search:
        coffees = coffees.filter(
            Q(name__icontains=search)
            | Q(coffee_bean__name__icontains=search)
            | Q(description__icontains=search)
            | Q(coffee_bean__flavor_notes__icontains=search)
        )
        print(f"After search filter ('{search}'): {coffees.count()} products")

    # Apply sorting
    sort_options = {
        "name": "name",
        "price_low": "price",
        "price_high": "-price",
        "newest": "-created_at",
        "rating": "-avg_rating",
    }

    if sort_by in sort_options:
        if sort_by == "rating":
            coffees = coffees.order_by("-avg_rating", "-review_count", "name")
        else:
            coffees = coffees.order_by(sort_options[sort_by])
        print(f"Applied sorting: {sort_by}")
    else:
        coffees = coffees.order_by("name")
        print(f"Applied default sorting: name")

    # Remove duplicates (in case of multiple categories per product)
    coffees = coffees.distinct()
    final_count = coffees.count()
    print(f"Final product count after distinct(): {final_count}")

    # Pagination
    paginator = Paginator(coffees, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Get filter options
    categories = CoffeeCategory.objects.all().order_by("name")
    roast_levels = RoastLevel.objects.all().order_by("name")
    bean_types = CoffeeBean.ORIGIN_CHOICES
    grind_types = CoffeeProduct.GRIND_CHOICES

    # Get category name for display
    category_name = None
    if category:
        try:
            category_obj = CoffeeCategory.objects.get(id=int(category))
            category_name = category_obj.name
        except (CoffeeCategory.DoesNotExist, ValueError, TypeError):
            pass

    context = {
        "page_obj": page_obj,
        "categories": categories,
        "roast_levels": roast_levels,
        "bean_types": bean_types,
        "grind_types": grind_types,
        "current_filters": {
            "category": category,
            "category_name": category_name,
            "roast": roast_level,
            "bean": bean_type,
            "grind": grind_type,
            "min_price": min_price,
            "max_price": max_price,
            "search": search,
            "sort": sort_by,
        },
    }

    return render(request, "coffee/coffee-list.html", context)


def coffee_detail_view(request, slug):
    """ໜ້າລາຍລະອຽດກາເຟ"""

    coffee = get_object_or_404(
        CoffeeProduct.objects.select_related(
            "coffee_bean", "roast_level"
        ).prefetch_related("categories", "reviews", "gallery_images"),
        slug=slug,
    )

    # ຣີວິວ
    reviews = coffee.reviews.all().order_by("-created_at")
    avg_rating = reviews.aggregate(Avg("rating"))["rating__avg"]
    review_count = reviews.count()

    # ກາເຟທີ່ຄ້າຍຄືກັນ
    similar_coffees = (
        CoffeeProduct.objects.filter(
            coffee_bean__origin=coffee.coffee_bean.origin, is_available=True
        )
        .exclude(slug=coffee.slug)
        .select_related("coffee_bean", "roast_level")[:4]
    )

    context = {
        "coffee": coffee,
        "reviews": reviews,
        "avg_rating": round(avg_rating, 1) if avg_rating else 0,
        "review_count": review_count,
        "similar_coffees": similar_coffees,
    }

    return render(request, "coffee/coffee-detail.html", context)


@require_http_methods(["POST"])
def add_review(request, slug):
    """ເພີ່ມຣີວິວ"""

    coffee = get_object_or_404(CoffeeProduct, slug=slug)

    if request.method == "POST":
        reviewer_name = request.POST.get("reviewer_name", "").strip()
        rating = request.POST.get("rating")
        comment = request.POST.get("comment", "").strip()

        # ກວດສອບຂໍ້ມູນ
        if not reviewer_name:
            messages.error(request, "ກະລຸນາປ້ອນຊື່ຜູ້ຣີວິວ")
            return redirect("coffee_detail", slug=slug)

        if not rating or not rating.isdigit() or int(rating) not in range(1, 6):
            messages.error(request, "ກະລຸນາໃຫ້ຄະແນນ 1-5 ດາວ")
            return redirect("coffee_detail", slug=slug)

        if not comment:
            messages.error(request, "ກະລຸນາປ້ອນຄຳເຫັນ")
            return redirect("coffee_detail", slug=slug)

        # ສ້າງຣີວິວ
        CoffeeReview.objects.create(
            coffee_product=coffee,
            reviewer_name=reviewer_name,
            rating=int(rating),
            comment=comment,
        )

        messages.success(request, "ເພີ່ມຣີວິວສຳເລັດແລ້ວ")

    return redirect("coffee_detail", slug=slug)


def category_view(request, category_id):
    """ໜ້າໝວດໝູ່ກາເຟ"""

    category = get_object_or_404(CoffeeCategory, pk=category_id)

    coffees = CoffeeProduct.objects.filter(
        categories=category, is_available=True
    ).select_related("coffee_bean", "roast_level")

    # Pagination
    paginator = Paginator(coffees, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "category": category,
        "page_obj": page_obj,
    }

    return render(request, "coffee/category.html", context)


def category_detail_view(request, slug):
    """ໜ້າລາຍລະອຽດໝວດໝູ່"""

    # Get the category
    category = get_object_or_404(CoffeeCategory, slug=slug)

    # Get sorting parameter
    sort_by = request.GET.get("sort", "name")

    # Base query for coffees in this category
    coffees = (
        CoffeeProduct.objects.filter(categories=category, is_available=True)
        .select_related("coffee_bean", "roast_level")
        .prefetch_related("reviews", "categories")
        .annotate(avg_rating=Avg("reviews__rating"), review_count=Count("reviews"))
    )

    # Apply sorting
    sort_options = {
        "name": "name",
        "price_low": "price",
        "price_high": "-price",
        "newest": "-created_at",
        "rating": "-avg_rating",
    }

    if sort_by in sort_options:
        if sort_by == "rating":
            coffees = coffees.order_by("-avg_rating", "-review_count")
        else:
            coffees = coffees.order_by(sort_options[sort_by])

    # Get price range for this category
    price_range = coffees.aggregate(min_price=Min("price"), max_price=Max("price"))

    # Pagination
    paginator = Paginator(coffees, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Get related categories (exclude current category)
    related_categories = (
        CoffeeCategory.objects.exclude(id=category.id)
        .annotate(products_count=Count("coffeeproduct"))
        .filter(products_count__gt=0)[:4]
    )

    context = {
        "category": category,
        "coffees": coffees,
        "page_obj": page_obj,
        "current_sort": sort_by,
        "price_range": price_range,
        "related_categories": related_categories,
    }

    return render(request, "coffee/category-detail.html", context)


def api_coffee_search(request):
    """API ສຳລັບຄົ້ນຫາກາເຟ (AJAX)"""

    query = request.GET.get("q", "").strip()

    if len(query) < 2:
        return JsonResponse({"results": []})

    coffees = CoffeeProduct.objects.filter(
        Q(name__icontains=query) | Q(coffee_bean__name__icontains=query),
        is_available=True,
    ).select_related("coffee_bean")[:10]

    results = []
    for coffee in coffees:
        results.append(
            {
                "id": coffee.id,
                "name": coffee.name,
                "bean_name": coffee.coffee_bean.name,
                "price": float(coffee.price),
                "image_url": (
                    coffee.image.url
                    if hasattr(coffee, "image") and coffee.image
                    else None
                ),
            }
        )

    return JsonResponse({"results": results})


def api_price_range(request):
    """API ສຳລັບດຶງຊ່ວງລາຄາ"""

    from django.db.models import Min, Max

    price_range = CoffeeProduct.objects.filter(is_available=True).aggregate(
        min_price=Min("price"), max_price=Max("price")
    )

    return JsonResponse(
        {
            "min_price": float(price_range["min_price"] or 0),
            "max_price": float(price_range["max_price"] or 0),
        }
    )


def compare_view(request):
    """ໜ້າເປີຍບທຽບກາເຟ"""

    coffee_ids = request.GET.getlist("compare")

    if not coffee_ids:
        messages.info(request, "ກະລຸນາເລືອກກາເຟທີ່ຕ້ອງການເປີຍບທຽບ")
        return redirect("coffee_list")

    coffees = (
        CoffeeProduct.objects.filter(id__in=coffee_ids, is_available=True)
        .select_related("coffee_bean", "roast_level")
        .prefetch_related("reviews")
    )

    # ຄຳນວນຂໍ້ມູນເພີ່ມເຕີມ
    coffee_data = []
    for coffee in coffees:
        avg_rating = coffee.reviews.aggregate(Avg("rating"))["rating__avg"]
        coffee_data.append(
            {
                "coffee": coffee,
                "avg_rating": round(avg_rating, 1) if avg_rating else 0,
                "review_count": coffee.reviews.count(),
            }
        )

    context = {
        "coffee_data": coffee_data,
    }

    return render(request, "coffee/compare.html", context)
