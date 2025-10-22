from django.contrib import admin
from django.utils.html import format_html
from .models import HeroSlide, VisitorCount


# Register your models here.
@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ("caption", "order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("caption",)


@admin.register(VisitorCount)
class VisitorCountAdmin(admin.ModelAdmin):
    list_display = ("count_display", "last_updated")
    readonly_fields = ("last_updated",)
    fields = ("count", "last_updated")

    def count_display(self, obj):
        """Display visitor count with formatting"""
        return format_html(
            '<span style="color: green; font-weight: bold; font-size: 16px;">{}</span>',
            f"{obj.count:,}"
        )
    count_display.short_description = "Total Visitors"

    def has_add_permission(self, request):
        """Prevent adding new records - only one should exist"""
        return not VisitorCount.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of visitor count"""
        return False
    

