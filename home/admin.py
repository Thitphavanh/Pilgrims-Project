from django.contrib import admin
from .models import HeroSlide


# Register your models here.
@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ("caption", "order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("caption",)
