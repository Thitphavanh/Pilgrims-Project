# Script to create realistic Lao customer reviews
from hotel.models import ReviewPlatform, GuestReview
from datetime import datetime, timedelta
from decimal import Decimal
import random

# Realistic Lao customer reviews
lao_reviews = [
    {
        "reviewer_name": "ນາງ ສົມພອນ",
        "review_text": "ໂຮງແຮມດີຫຼາຍ! ບໍລິການດີເລີດ ຫ້ອງພັກສະອາດ ແລະ ພະນັກງານເປັນມິດ. ຂ້ອຍຈະກັບມາອີກແນ່ນອນ.",
        "rating": Decimal("9.0"),
        "trip_type": "family",
    },
    {
        "reviewer_name": "ທ້າວ ບຸນເທົ່າ",
        "review_text": "ສະຖານທີ່ດີ ຢູ່ໃກ້ສູນກາງເມືອງ. ອາຫານເຊົ້າຫຼາກຫຼາຍ ແລະ ອ່ອຍ. ແຕ່ຫ້ອງນໍ້າຄວນປັບປຸງໃຫ້ດີຂຶ້ນ.",
        "rating": Decimal("7.5"),
        "trip_type": "business",
    },
    {
        "reviewer_name": "ນາງ ແສງດາວ",
        "review_text": "ບໍລິການດີຫຼາຍ! ຫ້ອງພັກກວ້າງຂວາງ ແລະ ສະອາດ. ທັດສະນະດີ ແລະ ພະນັກງານໃຫ້ຄວາມຊ່ວຍເຫຼືອດີ. ຄຸ້ມຄ່າສໍາລັບລາຄາ.",
        "rating": Decimal("9.5"),
        "trip_type": "couple",
    },
    {
        "reviewer_name": "ທ້າວ ວິໄຊ",
        "review_text": "ໂຮງແຮມດີ ແຕ່ເຄື່ອງປັບອາກາດມີສຽງດັງ. ບໍລິການປົກກະຕິ ແລະ ອາຫານເຊົ້າມີໃຫ້ເລືອກບໍ່ຫຼາຍ.",
        "rating": Decimal("6.0"),
        "trip_type": "solo",
    },
    {
        "reviewer_name": "ນາງ ພັນທິບ",
        "review_text": "ອິ່ນຈັຍ ໂຮງແຮມນີ້! ຫ້ອງສະອາດຫຼາຍ, Wi-Fi ໄວ, ແລະ ບໍລິການດີເລີດ. ລູກຄ້າບໍລິການດີ ແລະ ຍິ້ມແຍ້ມໃສ່ທຸກຄົນ.",
        "rating": Decimal("9.8"),
        "trip_type": "friends",
    },
    {
        "reviewer_name": "ທ້າວ ຄຳພອນ",
        "review_text": "ມີປະສົບການທີ່ດີ. ຫ້ອງພັກສະດວກສະບາຍ, ສະຖານທີ່ດີ, ແຕ່ຄວນມີບໍລິການຫ້ອງອາຫານດີກວ່ານີ້.",
        "rating": Decimal("8.0"),
        "trip_type": "business",
    },
    {
        "reviewer_name": "ນາງ ມະນີ",
        "review_text": "ໂຮງແຮມດີທີ່ສຸດທີ່ເຄີຍພັກ! ພະນັກງານໃສ່ໃຈລູກຄ້າຫຼາຍ, ຫ້ອງສະອາດ ແລະ ສິ່ງອຳນວຍຄວາມສະດວກຄົບຖ້ວນ.",
        "rating": Decimal("10.0"),
        "trip_type": "family",
    },
    {
        "reviewer_name": "ທ້າວ ສົມຊາຍ",
        "review_text": "ພໍໃຊ້ໄດ້ ແຕ່ລາຄາອາດແພງໄປໜ້ອຍ. ຫ້ອງພັກປົກກະຕິ ແລະ ບໍລິການກໍພໍໃຊ້ໄດ້.",
        "rating": Decimal("7.0"),
        "trip_type": "solo",
    },
]

# English reviews for international platforms
english_reviews = [
    {
        "reviewer_name": "Sarah Johnson",
        "review_text": "Excellent hotel with amazing service! The staff was incredibly friendly and helpful. The room was spacious, clean, and had a beautiful view. Will definitely stay here again.",
        "rating": Decimal("9.2"),
        "trip_type": "couple",
    },
    {
        "reviewer_name": "Mike Chen",
        "review_text": "Great location in the city center. Easy access to restaurants and attractions. The breakfast buffet was impressive with lots of local and international options.",
        "rating": Decimal("8.5"),
        "trip_type": "business",
    },
    {
        "reviewer_name": "Emma Williams",
        "review_text": "Perfect for families! The staff went above and beyond to make our kids feel welcome. Clean facilities, comfortable beds, and excellent value for money.",
        "rating": Decimal("9.7"),
        "trip_type": "family",
    },
    {
        "reviewer_name": "David Smith",
        "review_text": "Good hotel overall but some minor issues. Wi-Fi was a bit slow and the AC was noisy. However, the service was good and the location is convenient.",
        "rating": Decimal("7.8"),
        "trip_type": "business",
    },
    {
        "reviewer_name": "Lisa Brown",
        "review_text": "Outstanding experience! Everything was perfect from check-in to check-out. The room was immaculate, the staff was professional, and the amenities exceeded expectations.",
        "rating": Decimal("9.9"),
        "trip_type": "weekend",
    },
]

def create_sample_reviews():
    print("Creating sample reviews...")

    # Get or create platforms
    platforms = {}
    platform_names = ['agoda', 'booking', 'airbnb', 'google', 'expedia']

    for platform_name in platform_names:
        platform, created = ReviewPlatform.objects.get_or_create(
            name=platform_name,
            defaults={
                'display_name': platform_name.title(),
                'is_active': True,
                'brand_color': '#007bff' if platform_name == 'booking' else
                             '#ff5722' if platform_name == 'airbnb' else
                             '#ffc107' if platform_name == 'agoda' else
                             '#4285f4' if platform_name == 'google' else
                             '#003366',  # expedia
            }
        )
        platforms[platform_name] = platform
        if created:
            print(f"Created platform: {platform.display_name}")

    # Create reviews for different platforms
    review_count = 0

    # Add Lao reviews to Agoda (popular in Southeast Asia)
    for i, review_data in enumerate(lao_reviews):
        review_date = datetime.now() - timedelta(days=random.randint(1, 90))

        review = GuestReview.objects.create(
            platform=platforms['agoda'],
            reviewer_name=review_data['reviewer_name'],
            review_text=review_data['review_text'],
            rating=review_data['rating'],
            trip_type=review_data['trip_type'],
            review_date=review_date,
            is_active=True,
            is_verified=True,
            helpful_count=random.randint(0, 15)
        )
        review_count += 1
        print(f"Created Lao review: {review.reviewer_name} - {review.rating}/10")

    # Add English reviews to various platforms
    platform_keys = list(platforms.keys())
    for i, review_data in enumerate(english_reviews):
        platform_key = platform_keys[i % len(platform_keys)]
        review_date = datetime.now() - timedelta(days=random.randint(1, 120))

        review = GuestReview.objects.create(
            platform=platforms[platform_key],
            reviewer_name=review_data['reviewer_name'],
            review_text=review_data['review_text'],
            rating=review_data['rating'],
            trip_type=review_data['trip_type'],
            review_date=review_date,
            is_active=True,
            is_verified=True,
            helpful_count=random.randint(0, 25)
        )
        review_count += 1
        print(f"Created English review: {review.reviewer_name} - {review.rating}/10 on {platform_key}")

    print(f"\nTotal reviews created: {review_count}")
    return review_count

if __name__ == "__main__":
    create_sample_reviews()