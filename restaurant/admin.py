from django.contrib import admin
from .models import MenuItem
from django.utils.html import format_html


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "price",
        "is_featured",
        "image_preview",
        "created_at",
    )
    list_filter = ("category", "is_featured", "created_at")
    search_fields = ("name", "description")
    list_editable = ("is_featured", "price")
    prepopulated_fields = {"slug": ("name",)}  # Auto-generate slug from name

    # Organize fields in the edit form
    fieldsets = (
        ("Basic Information", {"fields": ("name", "slug", "description", "category")}),
        ("Pricing & Features", {"fields": ("price", "is_featured")}),
        ("Media", {"fields": ("image",)}),
    )

    # Custom methods
    def image_preview(self, obj):
        """Display image preview in admin list"""
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px;" />',
                obj.image.url,
            )
        return "No Image"

    image_preview.short_description = "Preview"

    # Add some styling to the admin
    class Media:
        css = {"all": ("admin/css/custom_admin.css",)}  # Optional: custom CSS

    # Actions
    actions = ["make_featured", "remove_featured"]

    def make_featured(self, request, queryset):
        """Mark selected items as featured"""
        updated = queryset.update(is_featured=True)
        self.message_user(
            request, f"{updated} menu items were successfully marked as featured."
        )

    make_featured.short_description = "Mark selected items as featured"

    def remove_featured(self, request, queryset):
        """Remove featured status from selected items"""
        updated = queryset.update(is_featured=False)
        self.message_user(
            request, f"{updated} menu items were successfully unmarked as featured."
        )

    remove_featured.short_description = "Remove featured status"
