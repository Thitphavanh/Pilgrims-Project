# coffee/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import *


@admin.register(CoffeeBean)
class CoffeeBeanAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "origin",
        "country",
        "region",
        "altitude",
        "acidity_level",
        "body_level",
    ]
    list_filter = ["origin", "country", "acidity_level", "body_level"]
    search_fields = ["name", "country", "region", "flavor_notes"]
    ordering = ["name"]

    fieldsets = (
        ("ຂໍ້ມູນພື້ນຖານ", {"fields": ("name", "origin", "country", "region", "altitude")}),
        ("ລົດຊາດແລະລັກສະນະ", {"fields": ("flavor_notes", "acidity_level", "body_level")}),
    )


@admin.register(RoastLevel)
class RoastLevelAdmin(admin.ModelAdmin):
    list_display = ["get_name_display", "description", "temperature_range"]
    ordering = ["name"]


class CoffeeReviewInline(admin.TabularInline):
    model = CoffeeReview
    extra = 0
    readonly_fields = ["created_at"]


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(CoffeeProduct)
class CoffeeProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "coffee_bean",
        "roast_level",
        "price",
        "weight_display",
        "stock_quantity",
        "is_available",
        "freshness_status",
    ]
    list_filter = [
        "is_available",
        "coffee_bean__origin",
        "roast_level",
        "grind_type",
        "weight_unit",
        "categories",
    ]
    search_fields = ["name", "coffee_bean__name", "description"]
    ordering = ["name"]
    filter_horizontal = ["categories"]
    inlines = [ProductImageInline, CoffeeReviewInline]

    fieldsets = (
        (
            "ຂໍ້ມູນພື້ນຖານ",
            {
                "fields": (
                    "name",
                    "coffee_bean",
                    "roast_level",
                    "grind_type",
                    "categories",
                    "images",
                    "slug",
                )
            },
        ),
        ("ນ້ຳໜັກແລະລາຄາ", {"fields": ("weight", "weight_unit", "price")}),
        ("ຄໍາອະທິບາຍແລະວິທີການຊົງ", {"fields": ("description", "brewing_method")}),
        ("ສະຕ໋ອກແລະສະຖານະ", {"fields": ("stock_quantity", "is_available")}),
        ("ວັນທີ", {"fields": ("roast_date", "expiry_date"), "classes": ("collapse",)}),
    )

    def weight_display(self, obj):
        return f"{obj.weight}{obj.weight_unit}"

    weight_display.short_description = "ນ້ຳໜັກ"

    def freshness_status(self, obj):
        if obj.is_fresh is None:
            return format_html('<span style="color: gray;">ບໍ່ລະບຸ</span>')
        elif obj.is_fresh:
            return format_html(
                '<span style="color: green; font-weight: bold;">ສົດ</span>'
            )
        else:
            return format_html('<span style="color: red;">ເບິດຄວາມສົດ</span>')

    freshness_status.short_description = "ຄວາມສົດ"

    def get_queryset(self, request):
        return (
            super().get_queryset(request).select_related("coffee_bean", "roast_level")
        )


@admin.register(CoffeeCategory)
class CoffeeCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "products_count"]
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name", "description"]

    def products_count(self, obj):
        return obj.coffeeproduct_set.filter(is_available=True).count()

    products_count.short_description = "Products Count"


@admin.register(CoffeeReview)
class CoffeeReviewAdmin(admin.ModelAdmin):
    list_display = ["coffee_product", "reviewer_name", "rating", "created_at"]
    list_filter = ["rating", "created_at", "coffee_product__coffee_bean__origin"]
    search_fields = ["reviewer_name", "comment", "coffee_product__name"]
    ordering = ["-created_at"]
    readonly_fields = ["created_at"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("coffee_product")


# การปรับแต่ง Admin site
admin.site.site_header = "Coffee Shop Administration"
admin.site.site_title = "Coffee Shop Admin"
admin.site.index_title = "ຍິນດີຕ້ອນຮັບສູ່ລະບົບຈັດການຮ້ານກາເຟ"
