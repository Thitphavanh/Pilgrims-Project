from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from hotel.models import ReviewPlatform, GuestReview


class Command(BaseCommand):
    help = "Import sample guest reviews"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=20,
            help="Number of sample reviews to create",
        )

    def handle(self, *args, **options):
        count = options["count"]

        # Sample review data
        sample_reviews = [
            {
                "reviewer_name": "Sarah M.",
                "review_text": "Absolutely wonderful experience! The international menu offers something for everyone, and the quality is exceptional. The staff went above and beyond to make our stay memorable.",
                "rating": 5.0,
                "trip_type": "family",
            },
            {
                "reviewer_name": "James & Lisa",
                "review_text": "The restaurant is a highlight of this property. We tried dishes from multiple cuisines and everything was perfectly prepared. The breakfast spread is incredible!",
                "rating": 5.0,
                "trip_type": "business",
            },
            {
                "reviewer_name": "Michael R.",
                "review_text": "Outstanding dining experience! The chef's specials are creative and delicious. Service is attentive without being intrusive. Will definitely return!",
                "rating": 4.5,
                "trip_type": "solo",
            },
            {
                "reviewer_name": "Emma & David",
                "review_text": "Absolutely stunning property! The host was incredibly accommodating and the restaurant exceeded all expectations. Perfect location and amazing amenities.",
                "rating": 5.0,
                "trip_type": "weekend",
            },
            {
                "reviewer_name": "Jennifer K.",
                "review_text": "Beautiful rooms and excellent service. The international restaurant menu is diverse and delicious. Staff were very helpful with local recommendations.",
                "rating": 4.8,
                "trip_type": "couple",
            },
            {
                "reviewer_name": "Robert & Family",
                "review_text": "Perfect for families! The kids loved the breakfast options and the staff made sure everyone was comfortable. Great value for money.",
                "rating": 4.7,
                "trip_type": "family",
            },
            {
                "reviewer_name": "Chen Wei",
                "review_text": "Exceptional hospitality and world-class dining. The fusion of international cuisines is expertly executed. A true culinary destination.",
                "rating": 5.0,
                "trip_type": "business",
            },
            {
                "reviewer_name": "Maria G.",
                "review_text": "Lovely stay with friends. The restaurant's variety means everyone found something they loved. Cocktails at the bar were also excellent.",
                "rating": 4.6,
                "trip_type": "friends",
            },
        ]

        platforms = list(ReviewPlatform.objects.filter(is_active=True))

        if not platforms:
            self.stdout.write(
                self.style.ERROR(
                    "No active platforms found. Run setup_review_platforms first."
                )
            )
            return

        created_count = 0

        for i in range(count):
            # Select random review template and platform
            review_template = random.choice(sample_reviews)
            platform = random.choice(platforms)

            # Create review with random date (last 3 months)
            days_ago = random.randint(1, 90)
            review_date = timezone.now() - timedelta(days=days_ago)

            # Add some variation to ratings
            rating_variation = random.uniform(-0.3, 0.1)
            rating = max(1.0, min(5.0, review_template["rating"] + rating_variation))

            # Special handling for Airbnb
            is_superhost = platform.name == "airbnb" and random.choice([True, False])

            review = GuestReview.objects.create(
                platform=platform,
                reviewer_name=review_template["reviewer_name"],
                review_text=review_template["review_text"],
                rating=round(rating, 1),
                trip_type=review_template["trip_type"],
                review_date=review_date,
                is_featured=random.choice([True, False]) if i < 5 else False,
                is_verified=True,
                is_superhost_review=is_superhost,
                helpful_count=random.randint(0, 15),
            )

            created_count += 1

            if created_count % 5 == 0:
                self.stdout.write(f"Created {created_count} reviews...")

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {created_count} sample reviews!")
        )
