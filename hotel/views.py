from .models import *
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Prefetch
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from django.utils import timezone
from datetime import datetime, timedelta


def hotel(request):
    """Room list page with available rooms, filters, and search functionality"""

    # Get query parameters for filtering
    room_type_filter = request.GET.get("room_type")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    capacity_filter = request.GET.get("capacity")
    view_type_filter = request.GET.get("view_type")
    amenity_filter = request.GET.get("amenity")

    # Base queryset - available rooms only
    rooms = (
        Room.objects.filter(is_out_of_order=False, check_in_date="")
        .select_related("room_type")
        .prefetch_related("amenities", "room_images", "roomamenity_set__amenity")
    )

    # Apply filters
    if room_type_filter:
        rooms = rooms.filter(room_type__id=room_type_filter)

    if min_price:
        try:
            rooms = rooms.filter(room_type__price_per_night__gte=float(min_price))
        except ValueError:
            pass

    if max_price:
        try:
            rooms = rooms.filter(room_type__price_per_night__lte=float(max_price))
        except ValueError:
            pass

    if capacity_filter:
        try:
            rooms = rooms.filter(room_type__capacity__gte=int(capacity_filter))
        except ValueError:
            pass

    # view_type filter removed as field no longer exists
    # if view_type_filter:
    #     rooms = rooms.filter(view_type=view_type_filter)

    if amenity_filter:
        rooms = rooms.filter(amenities__id=amenity_filter)

    # Order by featured rooms first, then by price
    rooms = rooms.order_by("-room_type__is_featured", "room_type__price_per_night")

    # Get data for filter dropdowns
    room_types = RoomType.objects.all().order_by("name")
    available_amenities = (
        Amenity.objects.filter(
            is_active=True, rooms__is_out_of_order=False
        )
        .distinct()
        .order_by("name")
    )

    # Get price range for slider
    price_range = RoomType.objects.aggregate(
        min_price=models.Min("price_per_night"), max_price=models.Max("price_per_night")
    )

    # Get featured rooms for highlights
    featured_rooms = rooms.filter(room_type__is_featured=True)[:3]

    # Get reviews (keeping your original logic)
    reviews = Review.objects.filter(is_approved=True).order_by("-date_posted")[:5]

    # Room statistics
    room_stats = {
        "total_available": rooms.count(),
        "room_types_count": room_types.count(),
        "avg_price": RoomType.objects.aggregate(avg=models.Avg("price_per_night"))[
            "avg"
        ],
    }

    context = {
        "rooms": rooms,
        "featured_rooms": featured_rooms,
        "room_types": room_types,
        "available_amenities": available_amenities,
        "reviews": reviews,
        "room_stats": room_stats,
        "price_range": price_range,
        # Current filter values for maintaining state
        "current_filters": {
            "room_type": room_type_filter,
            "min_price": min_price,
            "max_price": max_price,
            "capacity": capacity_filter,
            "view_type": view_type_filter,
            "amenity": amenity_filter,
        },
        # Choices for dropdowns
        "capacity_choices": [(i, f"{i}+ Guests") for i in range(1, 11)],
    }

    return render(request, "hotel/hotel.html", context)


def rooms_list_view(request):
    """Display list of all available rooms"""

    # Filter parameters
    room_type_filter = request.GET.get("type")
    # floor_filter = request.GET.get("floor")  # Removed as floor field no longer exists
    availability_filter = request.GET.get("available")
    price_min = request.GET.get("price_min")
    price_max = request.GET.get("price_max")

    # Base queryset
    rooms = Room.objects.select_related("room_type").all()

    # Apply filters
    if room_type_filter:
        rooms = rooms.filter(room_type__id=room_type_filter)

    # if floor_filter:
    #     rooms = rooms.filter(floor=floor_filter)  # Removed as floor field no longer exists

    if availability_filter == "true":
        rooms = rooms.filter(is_out_of_order=False)
    elif availability_filter == "false":
        rooms = rooms.filter(is_out_of_order=True)

    if price_min:
        try:
            rooms = rooms.filter(room_type__price_per_night__gte=float(price_min))
        except ValueError:
            pass

    if price_max:
        try:
            rooms = rooms.filter(room_type__price_per_night__lte=float(price_max))
        except ValueError:
            pass

    # Get filter options
    room_types = RoomType.objects.all()
    # floors = Room.objects.values_list("floor", flat=True).distinct().order_by("floor")  # Removed as floor field no longer exists
    floors = []  # Empty list since floor field is removed

    # Pagination
    from django.core.paginator import Paginator

    paginator = Paginator(rooms, 12)  # 12 rooms per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "room_types": room_types,
        "floors": floors,
        "current_filters": {
            "type": room_type_filter,
            # "floor": floor_filter,  # Removed as floor field no longer exists
            "available": availability_filter,
            "price_min": price_min,
            "price_max": price_max,
        },
        "page_title": "All Rooms & Suites",
    }

    return render(request, "hotel/rooms-list.html", context)


def room_detail_view(request, slug):
    """Display detailed information about a specific room"""

    # Get the room with related data
    room = get_object_or_404(Room, slug=slug)

    room_images = room.room_images.all().order_by("-is_primary", "id")

    # Get primary image or first available image
    primary_image = room_images.filter(is_primary=True).first()
    if not primary_image and room_images.exists():
        primary_image = room_images.first()

    # Get room amenities with additional info
    room_amenities_data = []
    premium_amenities_data = []
    standard_amenities_data = []

    for room_amenity in RoomAmenity.objects.filter(
        room=room, is_available=True
    ).select_related("amenity"):
        amenity_data = {
            "amenity": room_amenity.amenity,
            "additional_info": room_amenity.additional_info,
            "description": room_amenity.additional_info
            or room_amenity.amenity.description,
        }

        room_amenities_data.append(amenity_data)

        if room_amenity.amenity.is_premium:
            premium_amenities_data.append(amenity_data)
        else:
            standard_amenities_data.append(amenity_data)

    # Get related hotels (hotels that have rooms of the same type)
    related_hotels = (
        Hotel.objects.filter(room__room_type=room.room_type)
        .exclude(room=room)
        .distinct()[:4]
    )  # Limit to 4 related hotels

    # Get other rooms of the same type (alternatives)
    similar_rooms = Room.objects.filter(
        room_type=room.room_type, is_out_of_order=False, check_in_date=""
    ).exclude(id=room.id)[:3]

    context = {
        "room": room,
        "room_images": room_images,
        "primary_image": primary_image,
        "room_amenities_data": room_amenities_data,
        "premium_amenities_data": premium_amenities_data,
        "standard_amenities_data": standard_amenities_data,
        "related_hotels": related_hotels,
        "similar_rooms": similar_rooms,
        "page_title": f"{room.room_type.name} - Room {room.id}",
    }

    return render(request, "hotel/room-detail.html", context)


def review(request):
    # Get active platforms with their ratings and categories
    platforms = (
        ReviewPlatform.objects.filter(is_active=True)
        .prefetch_related(
            Prefetch("rating"),
            Prefetch("category_ratings__category"),
            Prefetch(
                "reviews",
                queryset=GuestReview.objects.filter(is_active=True).order_by(
                    "-review_date"
                )[:1],
            ),  # Latest review per platform
        )
        .order_by("display_order")
    )

    # Get recent reviews across all platforms
    recent_reviews = (
        GuestReview.objects.filter(is_active=True, platform__is_active=True)
        .select_related("platform")
        .order_by("-review_date")[:6]
    )

    # Get or create review summary
    review_summary, created = ReviewSummary.objects.get_or_create(
        defaults={"total_reviews": 0, "average_rating": 0.0}
    )

    # Calculate featured reviews (highest rated, most recent)
    featured_reviews = (
        GuestReview.objects.filter(
            is_active=True, is_featured=True, platform__is_active=True
        )
        .select_related("platform")
        .order_by("-rating", "-review_date")[:3]
    )

    # If no featured reviews, get top-rated recent ones
    if not featured_reviews:
        featured_reviews = (
            GuestReview.objects.filter(
                is_active=True, platform__is_active=True, rating__gte=9.0
            )
            .select_related("platform")
            .order_by("-rating", "-review_date")[:3]
        )

    context = {
        "platforms": platforms,
        "recent_reviews": recent_reviews,
        "featured_reviews": featured_reviews,
        "review_summary": review_summary,
        "page_title": "Guest Reviews & Ratings",
    }

    return render(request, "hotel/review.html", context)


@require_http_methods(["POST"])
def room_booking_view(request, slug):
    """Handle room booking form submission"""

    room = get_object_or_404(Room, slug=slug)

    if not room.is_available_for_booking:
        messages.error(request, "Sorry, this room is not available for booking.")
        return redirect("room-detail-page", slug=slug)

    # Get form data
    check_in_str = request.POST.get("check_in")
    check_out_str = request.POST.get("check_out")
    guests = request.POST.get("guests")
    special_requests = request.POST.get("special_requests", "")

    # Validate dates
    try:
        check_in = datetime.strptime(check_in_str, "%Y-%m-%d").date()
        check_out = datetime.strptime(check_out_str, "%Y-%m-%d").date()

        if check_in < timezone.now().date():
            messages.error(request, "Check-in date cannot be in the past.")
            return redirect("room-detail-page", slug=slug)

        if check_out <= check_in:
            messages.error(request, "Check-out date must be after check-in date.")
            return redirect("room-detail-page", slug=slug)

        if int(guests) > room.room_type.capacity:
            messages.error(
                request,
                f"This room can accommodate maximum {room.room_type.capacity} guests.",
            )
            return redirect("room-detail-page", slug=slug)

    except (ValueError, TypeError):
        messages.error(request, "Please provide valid dates and guest count.")
        return redirect("room-detail-page", slug=slug)

    # Calculate booking details
    nights = (check_out - check_in).days
    room_total = room.room_type.price_per_night * nights
    service_fee = 15 * nights
    taxes = 12 * nights
    total_amount = room_total + service_fee + taxes

    # Here you would typically create a booking record
    # For now, we'll just show a success message

    # Send confirmation email (optional)
    if hasattr(settings, "EMAIL_HOST") and settings.EMAIL_HOST:
        try:
            send_mail(
                subject="Room Booking Confirmation",
                message=f"""
                Dear Guest,
                
                Thank you for your booking request!
                
                Booking Details:
                - Room: {room.room_type.name} (Room {room.id})
                - Check-in: {check_in.strftime('%B %d, %Y')}
                - Check-out: {check_out.strftime('%B %d, %Y')}
                - Guests: {guests}
                - Total Amount: ${total_amount}
                
                We will contact you shortly to confirm your reservation.
                
                Best regards,
                Hotel Management
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[
                    (
                        request.user.email
                        if request.user.is_authenticated
                        else "guest@example.com"
                    )
                ],
                fail_silently=True,
            )
        except:
            pass

    messages.success(
        request,
        f"Booking request submitted successfully! "
        f'Total: ${total_amount} for {nights} night{"s" if nights != 1 else ""}. '
        f"We will contact you shortly to confirm your reservation.",
    )

    return redirect("room-detail-page", slug=slug)


@require_http_methods(["POST"])
def room_check_in_view(request, slug):
    """Handle room check-in"""
    room = get_object_or_404(Room, slug=slug)

    # Get form data
    check_in_date = request.POST.get("check_in_date", "").strip()
    check_out_date = request.POST.get("check_out_date", "").strip()

    # Validate required fields
    if not check_in_date:
        messages.error(request, "Check-in date is required.")
        return redirect("room-detail-page", slug=slug)

    # Attempt check-in
    try:
        room.check_in_guest(check_in_date, check_out_date)
        messages.success(
            request,
            f"Successfully checked in guest to Room {room.id}."
        )
    except ValueError as e:
        messages.error(request, str(e))

    return redirect("room-detail-page", slug=slug)


@require_http_methods(["POST"])
def room_check_out_view(request, slug):
    """Handle room check-out"""
    room = get_object_or_404(Room, slug=slug)

    # Attempt check-out
    try:
        room.check_out_guest()
        messages.success(
            request,
            f"Successfully checked out guest from Room {room.id}."
        )
    except ValueError as e:
        messages.error(request, str(e))

    return redirect("room-detail-page", slug=slug)


def room_availability_api(request):
    """API endpoint to check room availability"""

    if request.method == "GET":
        room_id = request.GET.get("room_id")
        check_in = request.GET.get("check_in")
        check_out = request.GET.get("check_out")

        try:
            room = Room.objects.get(id=room_id)

            # Here you would implement actual availability checking
            # For now, we'll just return the room's current availability status

            return JsonResponse(
                {
                    "available": not room.is_out_of_order,
                    "room_id": room.id,
                    "room_type": room.room_type.name,
                    "price_per_night": float(room.room_type.price_per_night),
                }
            )

        except Room.DoesNotExist:
            return JsonResponse({"error": "Room not found"}, status=404)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def featured_rooms_view(request):
    """Get featured rooms for homepage"""

    featured_rooms = Room.objects.filter(is_out_of_order=False, check_in_date="").select_related("room_type")[
        :6
    ]  # Get 6 featured rooms

    context = {
        "featured_rooms": featured_rooms,
    }

    return render(request, "hotel/featured-rooms.html", context)


def platform_detail(request, platform_name):
    """Detailed view for a specific platform's reviews"""

    platform = get_object_or_404(ReviewPlatform, name=platform_name, is_active=True)

    # Get platform rating and category ratings
    try:
        platform_rating = platform.rating
    except PlatformRating.DoesNotExist:
        platform_rating = None

    category_ratings = (
        CategoryRating.objects.filter(platform=platform)
        .select_related("category")
        .order_by("category__display_order")
    )

    # Get reviews for this platform
    reviews = GuestReview.objects.filter(platform=platform, is_active=True).order_by(
        "-review_date"
    )

    # Pagination
    from django.core.paginator import Paginator

    paginator = Paginator(reviews, 10)  # 10 reviews per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "platform": platform,
        "platform_rating": platform_rating,
        "category_ratings": category_ratings,
        "reviews": page_obj,
        "page_title": f"{platform.display_name} Reviews",
    }

    return render(request, "hotel/platform-detail.html", context)


def review_api(request):
    """API endpoint for AJAX requests"""

    if request.method == "GET":
        action = request.GET.get("action")

        if action == "platform_stats":
            platform_id = request.GET.get("platform_id")
            try:
                platform = ReviewPlatform.objects.get(id=platform_id, is_active=True)
                platform_rating = platform.rating
                category_ratings = CategoryRating.objects.filter(
                    platform=platform
                ).select_related("category")

                data = {
                    "platform_name": platform.display_name,
                    "overall_rating": float(platform_rating.overall_rating),
                    "total_reviews": platform_rating.total_reviews,
                    "categories": [
                        {
                            "name": cr.category.name,
                            "rating": float(cr.rating),
                            "percentage": cr.rating_percentage,
                        }
                        for cr in category_ratings
                    ],
                }
                return JsonResponse(data)
            except (ReviewPlatform.DoesNotExist, PlatformRating.DoesNotExist):
                return JsonResponse({"error": "Platform not found"}, status=404)

        elif action == "recent_reviews":
            platform_name = request.GET.get("platform")
            limit = int(request.GET.get("limit", 5))

            reviews_query = GuestReview.objects.filter(
                is_active=True, platform__is_active=True
            ).select_related("platform")

            if platform_name:
                reviews_query = reviews_query.filter(platform__name=platform_name)

            reviews = reviews_query.order_by("-review_date")[:limit]

            data = {
                "reviews": [
                    {
                        "reviewer_name": review.reviewer_name,
                        "rating": float(review.rating),
                        "review_text": review.review_text,
                        "trip_type": review.get_trip_type_display(),
                        "days_ago": review.days_ago,
                        "platform_name": review.platform.display_name,
                        "platform_color": review.platform.brand_color,
                        "is_superhost": review.is_superhost_review,
                    }
                    for review in reviews
                ]
            }
            return JsonResponse(data)

    return JsonResponse({"error": "Invalid request"}, status=400)


# Additional utility views


def reviews_widget(request):
    """Small widget showing overall rating for embedding"""

    review_summary = ReviewSummary.objects.first()
    if not review_summary:
        review_summary = ReviewSummary.objects.create()

    context = {
        "review_summary": review_summary,
    }

    return render(request, "hotel/rating-widget.html", context)


def platform_redirect(request, platform_name):
    """Redirect to actual platform URL"""

    platform = get_object_or_404(ReviewPlatform, name=platform_name, is_active=True)

    if platform.website_url:
        from django.shortcuts import redirect

        return redirect(platform.website_url)
    else:
        # Fallback to platform detail page
        return platform_detail(request, platform_name)


# Admin helper views (for staff only)

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages


@staff_member_required
def update_platform_stats(request, platform_id):
    """Admin view to manually update platform statistics"""

    platform = get_object_or_404(ReviewPlatform, id=platform_id)

    if request.method == "POST":
        try:
            # Update platform rating
            overall_rating = float(request.POST.get("overall_rating", 0))
            total_reviews = int(request.POST.get("total_reviews", 0))

            platform_rating, created = PlatformRating.objects.get_or_create(
                platform=platform,
                defaults={
                    "overall_rating": overall_rating,
                    "total_reviews": total_reviews,
                },
            )

            if not created:
                platform_rating.overall_rating = overall_rating
                platform_rating.total_reviews = total_reviews
                platform_rating.save()

            # Update category ratings
            categories = ReviewCategory.objects.filter(platform=platform)
            for category in categories:
                rating_value = float(request.POST.get(f"category_{category.id}", 0))
                if rating_value > 0:
                    CategoryRating.objects.update_or_create(
                        platform=platform,
                        category=category,
                        defaults={"rating": rating_value},
                    )

            # Update review summary
            summary = ReviewSummary.objects.first()
            if summary:
                summary.save()  # This will trigger the calculate_summary method

            messages.success(
                request, f"{platform.display_name} stats updated successfully!"
            )

        except (ValueError, TypeError) as e:
            messages.error(request, f"Error updating stats: {str(e)}")

    from django.shortcuts import redirect

    return redirect("admin:reviews_reviewplatform_change", platform_id)


@staff_member_required
def bulk_import_reviews(request):
    """Admin view for bulk importing reviews from CSV"""

    if request.method == "POST" and request.FILES.get("csv_file"):
        import csv
        import io

        csv_file = request.FILES["csv_file"]
        data_set = csv_file.read().decode("UTF-8")
        io_string = io.StringIO(data_set)

        reader = csv.DictReader(io_string)

        created_count = 0
        error_count = 0

        for row in reader:
            try:
                platform = ReviewPlatform.objects.get(name=row["platform"])

                GuestReview.objects.create(
                    platform=platform,
                    reviewer_name=row["reviewer_name"],
                    review_text=row["review_text"],
                    rating=float(row["rating"]),
                    trip_type=row.get("trip_type", "other"),
                    is_verified=row.get("is_verified", "true").lower() == "true",
                )
                created_count += 1

            except Exception as e:
                error_count += 1
                print(f"Error importing row: {e}")

        messages.success(
            request,
            f"Successfully imported {created_count} reviews. {error_count} errors.",
        )

    return render(request, "hotel/bulk-import.html")
