from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.urls import path, reverse
from django.shortcuts import redirect
from django.contrib import messages
from .models import (
    ReviewPlatform,
    ReviewCategory,
    PlatformRating,
    CategoryRating,
    GuestReview,
    ReviewSummary,
)


# @admin.register(Hotel)
# class HotelAdmin(admin.ModelAdmin):
#     list_display = ["name", "description"]


# @admin.register(RoomType)
# class RoomTypeAdmin(admin.ModelAdmin):
#     list_display = ["name", "description"]


# @admin.register(Room)
# class RoomAdmin(admin.ModelAdmin):
#     list_display = ["room_number"]


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "price_per_night",
        "capacity",
        "size_sqm",
        "amenities_summary",
        "rooms_count",
        "is_featured",
    ]
    list_filter = [
        "capacity",
        "is_featured",
        "has_wifi",
        "has_ac",
        "has_tv",
        "has_balcony",
    ]
    search_fields = ["name", "description"]
    ordering = ["price_per_night", "name"]

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("name", "description", "price_per_night", "capacity")},
        ),
        (
            "Room Specifications",
            {
                "fields": ("size_sqm", "bed_type"),
            },
        ),
        (
            "Amenities",
            {
                "fields": (
                    "has_wifi",
                    "has_ac",
                    "has_tv",
                    "has_balcony",
                    "has_kitchenette",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Management",
            {
                "fields": ("is_featured",),
            },
        ),
    )

    def amenities_summary(self, obj):
        amenities = []
        if obj.has_wifi:
            amenities.append('<i class="fas fa-wifi" title="WiFi"></i>')
        if obj.has_ac:
            amenities.append('<i class="fas fa-snowflake" title="A/C"></i>')
        if obj.has_tv:
            amenities.append('<i class="fas fa-tv" title="TV"></i>')
        if obj.has_balcony:
            amenities.append('<i class="fas fa-door-open" title="Balcony"></i>')
        if obj.has_kitchenette:
            amenities.append('<i class="fas fa-utensils" title="Kitchenette"></i>')

        return format_html(" ".join(amenities)) if amenities else "-"

    amenities_summary.short_description = "Amenities"

    def rooms_count(self, obj):
        count = obj.rooms.count()
        operational_count = obj.rooms.filter(is_out_of_order=False).count()

        url = reverse("admin:hotel_room_changelist") + f"?room_type__id__exact={obj.id}"
        return format_html(
            '<a href="{}">{} total ({} operational)</a>', url, count, operational_count
        )

    rooms_count.short_description = "Rooms"

    actions = ["mark_featured", "unmark_featured"]

    def mark_featured(self, request, queryset):
        count = queryset.update(is_featured=True)
        self.message_user(request, f"{count} room types marked as featured.")

    mark_featured.short_description = "Mark as featured"

    def unmark_featured(self, request, queryset):
        count = queryset.update(is_featured=False)
        self.message_user(request, f"{count} room types removed from featured.")

    unmark_featured.short_description = "Remove from featured"


class RoomAmenityInline(admin.TabularInline):
    model = RoomAmenity
    extra = 1
    fields = ("amenity", "is_available", "additional_info")


class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1
    fields = ("image", "alt_text", "is_primary")


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "room_type",
        "slug",
        "availability_status_display",
        "image_preview",
        "last_cleaned",
        "check_in_date",
        "check_out_date",
    ]
    list_filter = [
        "room_type",
        "is_out_of_order",
        "last_cleaned",
    ]
    search_fields = ["room_type__name", "maintenance_notes", "slug"]
    ordering = ["room_type", "id"]
    readonly_fields = ["slug"]

    inlines = [RoomImageInline, RoomAmenityInline]

    def amenities_count(self, obj):
        return obj.amenities.count()

    amenities_count.short_description = "Amenities"

    def slug_display(self, obj):
        if obj.slug:
            return obj.slug
        else:
            return "Auto-generated on save"

    slug_display.short_description = "Slug"

    fieldsets = (
        (
            "Basic Information",
            {
                "fields": (
                    "room_type",
                    "slug",
                    "check_in_date",
                    "check_out_date",
                )
            },
        ),
        (
            "Media",
            {
                "fields": ("image",),
            },
        ),
        (
            "Availability",
            {
                "fields": ("is_out_of_order",),
            },
        ),
        (
            "Maintenance",
            {"fields": ("last_cleaned", "maintenance_notes"), "classes": ("collapse",)},
        ),
    )

    readonly_fields = ["created_at", "updated_at"]

    def availability_status_display(self, obj):
        status = obj.availability_status
        if status == "Available":
            return format_html(
                '<span style="color: green; font-weight: bold;">'
                '<i class="fas fa-check-circle"></i> Available</span>'
            )
        elif status == "Occupied":
            return format_html(
                '<span style="color: orange; font-weight: bold;">'
                '<i class="fas fa-user"></i> Occupied</span>'
            )
        else:
            return format_html(
                '<span style="color: red; font-weight: bold;">'
                '<i class="fas fa-tools"></i> Out of Order</span>'
            )

    availability_status_display.short_description = "Status"

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />',
                obj.image.url,
            )
        return "-"

    image_preview.short_description = "Image"

    actions = [
        "mark_out_of_order",
        "mark_operational",
        "mark_cleaned_today",
        "regenerate_slugs",
    ]

    def mark_out_of_order(self, request, queryset):
        count = queryset.update(is_out_of_order=True)
        self.message_user(request, f"{count} rooms marked as out of order.")

    mark_out_of_order.short_description = "Mark as out of order"

    def mark_operational(self, request, queryset):
        count = queryset.update(is_out_of_order=False)
        self.message_user(request, f"{count} rooms marked as operational.")

    mark_operational.short_description = "Mark as operational"

    def mark_cleaned_today(self, request, queryset):
        from django.utils import timezone

        count = queryset.update(last_cleaned=timezone.now())
        self.message_user(request, f"{count} rooms marked as cleaned today.")

    mark_cleaned_today.short_description = "Mark as cleaned today"

    def regenerate_slugs(self, request, queryset):
        from django.utils.text import slugify

        updated_count = 0
        for room in queryset:
            if room.room_type:
                base_slug = slugify(f"{room.room_type.name}")
                slug = f"{base_slug}-{room.id}"
                counter = 1

                # Ensure uniqueness
                while Room.objects.filter(slug=slug).exclude(pk=room.pk).exists():
                    slug = f"{base_slug}-{room.id}-{counter}"
                    counter += 1

                room.slug = slug
                room.save()
                updated_count += 1

        self.message_user(request, f"Successfully regenerated slugs for {updated_count} rooms.")

    regenerate_slugs.short_description = "Regenerate slugs for selected rooms"


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name", "icon_color", "is_premium", "is_active", "rooms_count")
    list_filter = ("icon_color", "is_premium", "is_active")
    search_fields = ("name", "description")
    readonly_fields = ("created_at",)

    def rooms_count(self, obj):
        return obj.rooms.count()

    rooms_count.short_description = "Rooms"


@admin.register(RoomAmenity)
class RoomAmenityAdmin(admin.ModelAdmin):
    list_display = ("room", "amenity", "is_available")
    list_filter = ("is_available", "amenity__is_premium")
    search_fields = ("amenity__name",)


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "is_active",
        "features_summary",
        # "rooms_count_display",
        "contact_info",
        "image_preview",
    ]
    list_filter = [
        "is_active",
        "has_restaurant",
        "has_gym",
        "has_pool",
        "has_spa",
        "has_parking",
    ]
    search_fields = ["name", "description", "address"]
    ordering = ["name"]

    fieldsets = (
        ("Basic Information", {"fields": ("name", "description", "room", "is_active")}),
        (
            "Contact Information",
            {
                "fields": ("address", "phone", "email", "website"),
            },
        ),
        (
            "Media",
            {
                "fields": ("image",),
            },
        ),
        (
            "Features",
            {
                "fields": (
                    "has_restaurant",
                    "has_gym",
                    "has_pool",
                    "has_spa",
                    "has_parking",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    def features_summary(self, obj):
        features = []
        if obj.has_restaurant:
            features.append('<i class="fas fa-utensils" title="Restaurant"></i>')
        if obj.has_gym:
            features.append('<i class="fas fa-dumbbell" title="Gym"></i>')
        if obj.has_pool:
            features.append('<i class="fas fa-swimming-pool" title="Pool"></i>')
        if obj.has_spa:
            features.append('<i class="fas fa-spa" title="Spa"></i>')
        if obj.has_parking:
            features.append('<i class="fas fa-parking" title="Parking"></i>')

        return format_html(" ".join(features)) if features else "-"

    features_summary.short_description = "Features"

    # def rooms_count_display(self, obj):
    #     total_rooms = obj.hotels.count()
    #     available_rooms = obj.available_rooms_count

    #     return format_html("{} rooms ({} available)", total_rooms, available_rooms)

    # rooms_count_display.short_description = "Rooms"

    def contact_info(self, obj):
        info = []
        if obj.phone:
            info.append(f"📞 {obj.phone}")
        if obj.email:
            info.append(f"✉️ {obj.email}")
        return " | ".join(info) if info else "-"

    contact_info.short_description = "Contact"

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="40" style="object-fit: cover; border-radius: 4px;" />',
                obj.image.url,
            )
        return "-"

    image_preview.short_description = "Image"

    actions = ["activate_hotels", "deactivate_hotels"]

    def activate_hotels(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f"{count} hotels activated.")

    activate_hotels.short_description = "Activate selected hotels"

    def deactivate_hotels(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f"{count} hotels deactivated.")

    deactivate_hotels.short_description = "Deactivate selected hotels"


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "guest_name",
        "room",
        "check_in_date",
        "check_out_date",
        "guests_count",
        "total_amount",
        "status",
        "created_at",
    ]
    list_filter = [
        "status",
        "check_in_date",
        "check_out_date",
        "created_at",
        "room__room_type",
    ]
    search_fields = [
        "guest_name",
        "guest_email",
        "guest_phone",
        "room__room_type__name",
    ]
    date_hierarchy = "check_in_date"
    ordering = ["-created_at"]

    fieldsets = (
        ("Guest Information", {"fields": ("guest_name", "guest_email", "guest_phone")}),
        (
            "Booking Details",
            {
                "fields": (
                    "room",
                    "check_in_date",
                    "check_out_date",
                    "guests_count",
                    "special_requests",
                )
            },
        ),
        ("Financial", {"fields": ("total_amount",)}),
        ("Status", {"fields": ("status",)}),
        (
            "Metadata",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    readonly_fields = ["created_at", "updated_at"]

    actions = [
        "confirm_bookings",
        "check_in_guests",
        "check_out_guests",
        "cancel_bookings",
    ]

    def confirm_bookings(self, request, queryset):
        count = queryset.filter(status="pending").update(status="confirmed")
        self.message_user(request, f"{count} bookings confirmed.")

    confirm_bookings.short_description = "Confirm selected bookings"

    def check_in_guests(self, request, queryset):
        count = queryset.filter(status="confirmed").update(status="checked_in")
        self.message_user(request, f"{count} guests checked in.")

    check_in_guests.short_description = "Check in selected guests"

    def check_out_guests(self, request, queryset):
        count = queryset.filter(status="checked_in").update(status="checked_out")
        self.message_user(request, f"{count} guests checked out.")

    check_out_guests.short_description = "Check out selected guests"

    def cancel_bookings(self, request, queryset):
        count = queryset.exclude(status__in=["checked_out", "cancelled"]).update(
            status="cancelled"
        )
        self.message_user(request, f"{count} bookings cancelled.")

    cancel_bookings.short_description = "Cancel selected bookings"


# Custom admin site modifications
admin.site.site_header = "Hotel Management System"
admin.site.site_title = "Hotel Admin"
admin.site.index_title = "Welcome to Hotel Administration"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["name", "email"]


admin.site.register(ReviewPlatform)
# @admin.register(ReviewPlatform)
# class ReviewPlatformAdmin(admin.ModelAdmin):
#     list_display = [
#         "display_name",
#         "name",
#         "is_active",
#         "display_order",
#         "rating_info",
#         "review_count",
#     ]
#     list_filter = ["is_active", "name"]
#     search_fields = ["display_name", "name"]
#     ordering = ["display_order", "display_name"]

#     fieldsets = (
#         (
#             "Basic Information",
#             {"fields": ("name", "display_name", "is_active", "display_order")},
#         ),
#         ("Branding", {"fields": ("logo_url", "brand_color"), "classes": ("collapse",)}),
#         ("External Links", {"fields": ("website_url",), "classes": ("collapse",)}),
#     )

#     def rating_info(self, obj):
#         try:
#             rating = obj.rating
#             return format_html(
#                 '<span style="color: #ffc107;">★</span> {}/5.0', rating.overall_rating
#             )
#         except PlatformRating.DoesNotExist:
#             return format_html('<span style="color: #dc3545;">No rating</span>')

#     rating_info.short_description = "Current Rating"

#     def review_count(self, obj):
#         count = obj.reviews.filter(is_active=True).count()
#         return format_html(
#             '<a href="{}?platform__id__exact={}">{} reviews</a>',
#             reverse("admin:reviews_guestreview_changelist"),
#             obj.id,
#             count,
#         )

#     review_count.short_description = "Reviews"

#     actions = ["activate_platforms", "deactivate_platforms"]

#     def activate_platforms(self, request, queryset):
#         count = queryset.update(is_active=True)
#         self.message_user(request, f"{count} platforms activated.")

#     activate_platforms.short_description = "Activate selected platforms"

#     def deactivate_platforms(self, request, queryset):
#         count = queryset.update(is_active=False)
#         self.message_user(request, f"{count} platforms deactivated.")

#     deactivate_platforms.short_description = "Deactivate selected platforms"


@admin.register(ReviewCategory)
class ReviewCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "platform", "is_active", "display_order"]
    list_filter = ["platform", "is_active"]
    search_fields = ["name", "platform__display_name"]
    ordering = ["platform", "display_order", "name"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("platform")


class CategoryRatingInline(admin.TabularInline):
    model = CategoryRating
    extra = 0
    fields = ["category", "rating"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("category")


admin.site.register(PlatformRating)
# @admin.register(PlatformRating)
# class PlatformRatingAdmin(admin.ModelAdmin):
#     list_display = ["platform", "overall_rating", "total_reviews", "last_updated"]
#     list_filter = ["platform", "last_updated"]
#     readonly_fields = ["last_updated"]
#     inlines = [CategoryRatingInline]

#     fieldsets = (
#         (
#             "Rating Information",
#             {"fields": ("platform", "overall_rating", "total_reviews")},
#         ),
#         ("Metadata", {"fields": ("last_updated",), "classes": ("collapse",)}),
#     )

#     def get_queryset(self, request):
#         return super().get_queryset(request).select_related("platform")


@admin.register(CategoryRating)
class CategoryRatingAdmin(admin.ModelAdmin):
    list_display = ["platform", "category", "rating"]
    list_filter = ["platform", "category__name"]
    search_fields = ["platform__display_name", "category__name"]

    # def rating_bar(self, obj):
    #     percentage = obj.rating_percentage
    #     return format_html(
    #         '<div style="width: 100px; background-color: #e9ecef; border-radius: 4px;">'
    #         '<div style="width: {}%; background-color: #28a745; height: 20px; border-radius: 4px; '
    #         'text-align: center; color: white; font-size: 12px; line-height: 20px;">{:.1f}</div></div>',
    #         percentage,
    #         obj.rating,
    #     )

    # rating_bar.short_description = "Rating Visualization"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("platform", "category")


@admin.register(GuestReview)
class GuestReviewAdmin(admin.ModelAdmin):
    list_display = [
        "reviewer_name",
        "platform",
        "rating",
        "trip_type",
        "review_date",
        "is_featured",
        "is_verified",
        "is_active",
    ]
    list_filter = [
        "platform",
        "rating",
        "trip_type",
        "is_featured",
        "is_verified",
        "is_active",
        "review_date",
    ]
    search_fields = ["reviewer_name", "review_text", "platform__display_name"]
    date_hierarchy = "review_date"
    ordering = ["-review_date"]

    fieldsets = (
        (
            "Review Information",
            {"fields": ("platform", "reviewer_name", "rating", "review_text")},
        ),
        (
            "Trip Details",
            {
                "fields": ("trip_type", "review_date"),
            },
        ),
        (
            "Status & Features",
            {"fields": ("is_featured", "is_verified", "is_active", "helpful_count")},
        ),
        (
            "Special Attributes",
            {"fields": ("is_superhost_review",), "classes": ("collapse",)},
        ),
        (
            "Metadata",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    readonly_fields = ["created_at", "updated_at"]

    actions = [
        "mark_featured",
        "unmark_featured",
        "mark_verified",
        "mark_unverified",
        "activate_reviews",
        "deactivate_reviews",
    ]

    def mark_featured(self, request, queryset):
        count = queryset.update(is_featured=True)
        self.message_user(request, f"{count} reviews marked as featured.")

    mark_featured.short_description = "Mark as featured"

    def unmark_featured(self, request, queryset):
        count = queryset.update(is_featured=False)
        self.message_user(request, f"{count} reviews unmarked as featured.")

    unmark_featured.short_description = "Remove from featured"

    def mark_verified(self, request, queryset):
        count = queryset.update(is_verified=True)
        self.message_user(request, f"{count} reviews marked as verified.")

    mark_verified.short_description = "Mark as verified"

    def mark_unverified(self, request, queryset):
        count = queryset.update(is_verified=False)
        self.message_user(request, f"{count} reviews marked as unverified.")

    mark_unverified.short_description = "Mark as unverified"

    def activate_reviews(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f"{count} reviews activated.")

    activate_reviews.short_description = "Activate selected reviews"

    def deactivate_reviews(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f"{count} reviews deactivated.")

    deactivate_reviews.short_description = "Deactivate selected reviews"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("platform")


@admin.register(ReviewSummary)
class ReviewSummaryAdmin(admin.ModelAdmin):
    list_display = ["average_rating", "total_reviews", "last_updated"]
    readonly_fields = ["last_updated"]

    fieldsets = (
        ("Overall Statistics", {"fields": ("total_reviews", "average_rating")}),
        (
            "Featured Statistics",
            {
                "fields": (
                    ("featured_stat_1_label", "featured_stat_1_value"),
                    ("featured_stat_2_label", "featured_stat_2_value"),
                    ("featured_stat_3_label", "featured_stat_3_value"),
                )
            },
        ),
        ("Metadata", {"fields": ("last_updated",), "classes": ("collapse",)}),
    )

    def has_add_permission(self, request):
        # Only allow one ReviewSummary instance
        return not ReviewSummary.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    actions = ["recalculate_summary"]

    def recalculate_summary(self, request, queryset):
        for summary in queryset:
            summary.calculate_summary()
            summary.save()
        self.message_user(request, "Review summary recalculated.")

    recalculate_summary.short_description = "Recalculate summary statistics"


# Custom admin site modifications
admin.site.site_header = "Project Pilgrims Reviews Admin"
admin.site.site_title = "Reviews Admin"
admin.site.index_title = "Manage Guest Reviews & Ratings"
