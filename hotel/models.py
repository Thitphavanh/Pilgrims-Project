from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.utils.text import slugify
from decimal import Decimal


class RoomType(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField()

    # Additional fields for better room management
    size_sqm = models.PositiveIntegerField(
        default=25, help_text="Room size in square meters"
    )
    bed_type = models.CharField(max_length=50, default="Queen Bed")

    # Amenities (you can expand this)
    has_wifi = models.BooleanField(default=True)
    has_ac = models.BooleanField(default=True)
    has_tv = models.BooleanField(default=True)
    has_balcony = models.BooleanField(default=False)
    has_kitchenette = models.BooleanField(default=False)

    # Meta information
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ["price_per_night", "name"]
        verbose_name = "Room Type"
        verbose_name_plural = "Room Types"

    def __str__(self):
        return f"{self.name} - ${self.price_per_night}/night"


class Amenity(models.Model):
    """Model for room amenities"""

    ICON_COLOR_CHOICES = [
        ("blue", "Blue"),
        ("green", "Green"),
        ("purple", "Purple"),
        ("orange", "Orange"),
        ("red", "Red"),
        ("teal", "Teal"),
        ("pink", "Pink"),
        ("indigo", "Indigo"),
        ("yellow", "Yellow"),
        ("gray", "Gray"),
    ]

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)
    icon = models.CharField(
        max_length=50, help_text="FontAwesome icon class (e.g., fas fa-wifi)"
    )
    icon_color = models.CharField(
        max_length=20, choices=ICON_COLOR_CHOICES, default="blue"
    )
    is_premium = models.BooleanField(default=False, help_text="Mark as premium amenity")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Amenity"
        verbose_name_plural = "Amenities"

    def __str__(self):
        return self.name


class Room(models.Model):
    room_type = models.ForeignKey(
        RoomType, on_delete=models.CASCADE, related_name="rooms"
    )
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    amenities = models.ManyToManyField(
        Amenity, through="RoomAmenity", related_name="rooms", blank=True
    )
    image = models.ImageField(upload_to="rooms/", null=True, blank=True)

    # Check-in/out information
    check_in_date = models.CharField(max_length=20, blank=True, default="", help_text="Check-in date as text")
    check_out_date = models.CharField(max_length=20, blank=True, default="", help_text="Check-out date as text")

    # Maintenance and status
    last_cleaned = models.DateTimeField(null=True, blank=True)
    maintenance_notes = models.TextField(blank=True)
    is_out_of_order = models.BooleanField(default=False)

    # Meta information
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ["room_type", "id"]
        verbose_name = "Room"
        verbose_name_plural = "Rooms"

    def __str__(self):
        return f"Room {self.id} - {self.room_type.name}"

    def save(self, *args, **kwargs):
        """Override save to ensure slug is created"""
        if not self.slug:
            # Create base slug from room type and id
            if self.room_type:
                base_slug = slugify(f"{self.room_type.name}")
                # If we don't have an ID yet, save first to get one
                if not self.id:
                    super().save(*args, **kwargs)

                # Now create slug with ID
                slug = f"{base_slug}-{self.id}"
                counter = 1
                while Room.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                    slug = f"{base_slug}-{self.id}-{counter}"
                    counter += 1
                self.slug = slug
        super().save(*args, **kwargs)


    @property
    def total_price_with_fees(self):
        """Calculate total price including service fees and taxes"""
        base_price = self.room_type.price_per_night
        service_fee = 15
        taxes = 12
        return base_price + service_fee + taxes

    def get_available_amenities(self):
        """Get all available amenities for this room"""
        return self.amenities.filter(
            roomamenity__is_available=True, is_active=True
        ).order_by("name")

    def get_premium_amenities(self):
        """Get premium amenities for this room"""
        return self.get_available_amenities().filter(is_premium=True)

    def get_standard_amenities(self):
        """Get standard amenities for this room"""
        return self.get_available_amenities().filter(is_premium=False)

    def get_amenity_description(self, amenity):
        """Get room-specific description for an amenity"""
        try:
            room_amenity = self.roomamenity_set.get(amenity=amenity)
            return room_amenity.additional_info or amenity.description
        except RoomAmenity.DoesNotExist:
            return amenity.description

    def check_in_guest(self, check_in_date, check_out_date=None):
        """Check in a guest to this room"""
        if self.check_in_date:
            raise ValueError("Room is already booked")
        if self.is_out_of_order:
            raise ValueError("Room is out of order")

        self.check_in_date = check_in_date
        self.check_out_date = check_out_date or ""
        self.save()

    def check_out_guest(self):
        """Check out the current guest from this room"""
        if not self.check_in_date:
            raise ValueError("No guest is currently checked in")

        self.check_in_date = ""
        self.check_out_date = ""
        self.save()

    @property
    def is_available_for_booking(self):
        """Check if room is available for new bookings"""
        return not self.is_out_of_order and not self.check_in_date


class RoomImage(models.Model):
    room = models.ForeignKey(Room, related_name="room_images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="room/")
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"Room {self.room.id} - Image"


class RoomAmenity(models.Model):
    """Through model for Room-Amenity relationship with additional info"""

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    additional_info = models.CharField(
        max_length=200,
        blank=True,
        help_text="Extra details about this amenity for this room",
    )

    class Meta:
        unique_together = ("room", "amenity")
        verbose_name = "Room Amenity"
        verbose_name_plural = "Room Amenities"

    def __str__(self):
        return f"Room {self.room.id} - {self.amenity.name}"


class Hotel(models.Model):
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="hotels", null=True, blank=True
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="hotel/", null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    # Additional hotel information
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    # Hotel features
    has_restaurant = models.BooleanField(default=True)
    has_gym = models.BooleanField(default=False)
    has_pool = models.BooleanField(default=False)
    has_spa = models.BooleanField(default=False)
    has_parking = models.BooleanField(default=True)

    # Meta information
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Hotel Property"
        verbose_name_plural = "Hotel Properties"

    def __str__(self):
        return f"{self.name}"

    @property
    def available_rooms_count(self):
        """Count of available rooms in this hotel"""
        return self.hotels.filter(is_out_of_order=False).count()


# Optional: Booking model for future use
class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("checked_in", "Checked In"),
        ("checked_out", "Checked Out"),
        ("cancelled", "Cancelled"),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bookings")
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField()
    guest_phone = models.CharField(max_length=20, blank=True)

    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guests_count = models.PositiveIntegerField()

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    special_requests = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"

    def __str__(self):
        return f"Booking {self.id} - {self.guest_name} - Room {self.room.id}"

    @property
    def nights_count(self):
        return (self.check_out_date - self.check_in_date).days


class Review(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    comment = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.rating}/10 stars"


class ReviewPlatform(models.Model):
    """Model for review platforms like Agoda, Booking.com, Airbnb"""

    PLATFORM_CHOICES = [
        ("agoda", "Agoda"),
        ("booking", "Booking.com"),
        ("airbnb", "Airbnb"),
        ("tripadvisor", "TripAdvisor"),
        ("google", "Google Reviews"),
        ("expedia", "Expedia"),
    ]

    name = models.CharField(max_length=50, choices=PLATFORM_CHOICES, unique=True)
    display_name = models.CharField(max_length=100)
    logo_url = models.URLField(blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)
    brand_color = models.CharField(
        max_length=7, default="#000000", help_text="Hex color code"
    )
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "display_name"]
        verbose_name = "Review Platform"
        verbose_name_plural = "Review Platforms"

    def __str__(self):
        return self.display_name


class ReviewCategory(models.Model):
    """Categories for different types of reviews (Service, Cleanliness, etc.)"""

    name = models.CharField(max_length=100)
    platform = models.ForeignKey(
        ReviewPlatform, on_delete=models.CASCADE, related_name="categories"
    )
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["platform", "display_order", "name"]
        verbose_name = "Review Category"
        verbose_name_plural = "Review Categories"
        unique_together = ["name", "platform"]

    def __str__(self):
        return f"{self.platform.display_name} - {self.name}"


class PlatformRating(models.Model):
    """Overall ratings for each platform"""

    platform = models.OneToOneField(
        ReviewPlatform, on_delete=models.CASCADE, related_name="rating"
    )
    overall_rating = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        validators=[
            MinValueValidator(Decimal("0.0")),
            MaxValueValidator(Decimal("10.0")),
        ],
    )
    total_reviews = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Platform Rating"
        verbose_name_plural = "Platform Ratings"

    def __str__(self):
        return f"{self.platform.display_name} - {self.overall_rating}/10.0"


class CategoryRating(models.Model):
    """Ratings for specific categories within each platform"""

    platform = models.ForeignKey(
        ReviewPlatform, on_delete=models.CASCADE, related_name="category_ratings"
    )
    category = models.ForeignKey(ReviewCategory, on_delete=models.CASCADE)
    rating = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        validators=[
            MinValueValidator(Decimal("0.0")),
            MaxValueValidator(Decimal("10.0")),
        ],
    )

    class Meta:
        unique_together = ["platform", "category"]
        verbose_name = "Category Rating"
        verbose_name_plural = "Category Ratings"

    def __str__(self):
        return f"{self.platform.display_name} - {self.category.name}: {self.rating}"

    @property
    def rating_percentage(self):
        """Return rating as percentage for progress bars"""
        return (self.rating / 10.0) * 100


class GuestReview(models.Model):
    """Individual guest reviews"""

    TRIP_TYPE_CHOICES = [
        ("family", "Family Vacation"),
        ("business", "Business Trip"),
        ("solo", "Solo Traveler"),
        ("couple", "Couple's Trip"),
        ("friends", "Friends Trip"),
        ("weekend", "Weekend Getaway"),
        ("traveled", "Traveled with partner"),
        ("other", "Other"),
    ]

    platform = models.ForeignKey(
        ReviewPlatform, on_delete=models.CASCADE, related_name="reviews"
    )
    reviewer_name = models.CharField(max_length=100)
    review_text = models.TextField()
    rating = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        validators=[
            MinValueValidator(Decimal("0.0")),
            MaxValueValidator(Decimal("10.0")),
        ],
    )
    trip_type = models.CharField(
        max_length=25, choices=TRIP_TYPE_CHOICES, default="other"
    )
    review_date = models.DateTimeField(default=timezone.now)
    is_featured = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=True)
    helpful_count = models.PositiveIntegerField(default=0)

    # Airbnb specific fields
    is_superhost_review = models.BooleanField(default=False)

    # Admin fields
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-review_date", "-created_at"]
        verbose_name = "Guest Review"
        verbose_name_plural = "Guest Reviews"

    def __str__(self):
        return f"{self.reviewer_name} - {self.platform.display_name} ({self.rating}/10)"

    @property
    def days_ago(self):
        """Calculate days since review was posted"""
        delta = timezone.now() - self.review_date
        days = delta.days

        if days == 0:
            return "Today"
        elif days == 1:
            return "1 day ago"
        elif days < 7:
            return f"{days} days ago"
        elif days < 14:
            return "1 week ago"
        elif days < 30:
            weeks = days // 7
            return f"{weeks} weeks ago"
        elif days < 60:
            return "1 month ago"
        else:
            months = days // 30
            return f"{months} months ago"

    @property
    def star_range(self):
        """Return range for template star rendering"""
        return range(1, 11)  # 1 to 10

    @property
    def full_stars(self):
        """Return number of full stars"""
        return int(self.rating)

    @property
    def has_half_star(self):
        """Check if review has half star"""
        return (self.rating % 1) >= 0.5


class ReviewSummary(models.Model):
    """Overall review summary across all platforms"""

    total_reviews = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=Decimal("0.0"),
        validators=[
            MinValueValidator(Decimal("0.0")),
            MaxValueValidator(Decimal("10.0")),
        ],
    )
    last_updated = models.DateTimeField(auto_now=True)

    # Featured statistics
    featured_stat_1_label = models.CharField(
        max_length=100, default="Excellence Rating"
    )
    featured_stat_1_value = models.CharField(max_length=50, default="9.6/10")

    featured_stat_2_label = models.CharField(
        max_length=100, default="Guest Satisfaction"
    )
    featured_stat_2_value = models.CharField(max_length=50, default="98%")

    featured_stat_3_label = models.CharField(max_length=100, default="Repeat Guests")
    featured_stat_3_value = models.CharField(max_length=50, default="85%")

    class Meta:
        verbose_name = "Review Summary"
        verbose_name_plural = "Review Summary"

    def __str__(self):
        return f"Overall: {self.average_rating}/10.0 ({self.total_reviews} reviews)"

    def save(self, *args, **kwargs):
        # Auto-calculate summary stats
        self.calculate_summary()
        super().save(*args, **kwargs)

    def calculate_summary(self):
        """Calculate overall statistics from all platforms"""
        from django.db.models import Avg, Sum

        # Calculate total reviews
        self.total_reviews = (
            PlatformRating.objects.aggregate(total=Sum("total_reviews"))["total"] or 0
        )

        # Calculate weighted average rating
        if self.total_reviews > 0:
            platform_ratings = PlatformRating.objects.filter(total_reviews__gt=0)
            total_weighted_score = sum(
                float(pr.overall_rating) * pr.total_reviews for pr in platform_ratings
            )
            self.average_rating = Decimal(
                str(total_weighted_score / self.total_reviews)
            )
        else:
            self.average_rating = Decimal("0.0")
