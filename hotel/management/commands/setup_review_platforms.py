from django.core.management.base import BaseCommand
from hotel.models import ReviewPlatform, ReviewCategory, PlatformRating, CategoryRating

class Command(BaseCommand):
    help = 'Setup initial review platforms and categories'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Reset all platform data',
        )
    
    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write('Resetting platform data...')
            ReviewPlatform.objects.all().delete()
        
        # Platform data with configurations
        platforms_data = [
            {
                'name': 'agoda',
                'display_name': 'Agoda',
                'logo_url': 'https://cdn.worldota.net/t/1024x768/content/6f/22/6f22e0f5ad717b5e90bcea3ca8f34e4c8c8e2b5e.jpeg',
                'brand_color': '#FF6B35',
                'display_order': 1,
                'overall_rating': 4.7,
                'total_reviews': 1234,
                'categories': [
                    {'name': 'Service', 'rating': 9.4},
                    {'name': 'Cleanliness', 'rating': 9.6},
                    {'name': 'Location', 'rating': 9.2},
                ]
            },
            {
                'name': 'booking',
                'display_name': 'Booking.com',
                'logo_url': 'https://cf.bstatic.com/static/img/b26logo/rebrand/logo_blue_150px.png',
                'brand_color': '#003580',
                'display_order': 2,
                'overall_rating': 4.9,
                'total_reviews': 896,
                'categories': [
                    {'name': 'Staff', 'rating': 9.8},
                    {'name': 'Facilities', 'rating': 9.5},
                    {'name': 'Comfort', 'rating': 9.7},
                ]
            },
            {
                'name': 'airbnb',
                'display_name': 'Airbnb',
                'logo_url': 'https://a0.muscache.com/airbnb/static/logos/belo-200x200-4d851c5b28f61931bf1df28dd15e60ef.png',
                'brand_color': '#FF5A5F',
                'display_order': 3,
                'overall_rating': 4.9,
                'total_reviews': 342,
                'categories': [
                    {'name': 'Check-in', 'rating': 4.9},
                    {'name': 'Communication', 'rating': 4.8},
                    {'name': 'Accuracy', 'rating': 5.0},
                    {'name': 'Location', 'rating': 4.7},
                    {'name': 'Value', 'rating': 4.6},
                ]
            }
        ]
        
        for platform_data in platforms_data:
            # Create or update platform
            platform, created = ReviewPlatform.objects.get_or_create(
                name=platform_data['name'],
                defaults={
                    'display_name': platform_data['display_name'],
                    'logo_url': platform_data['logo_url'],
                    'brand_color': platform_data['brand_color'],
                    'display_order': platform_data['display_order'],
                    'is_active': True,
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created platform: {platform.display_name}')
                )
            
            # Create or update platform rating
            platform_rating, created = PlatformRating.objects.get_or_create(
                platform=platform,
                defaults={
                    'overall_rating': platform_data['overall_rating'],
                    'total_reviews': platform_data['total_reviews'],
                }
            )
            
            # Create categories and ratings
            for cat_data in platform_data['categories']:
                category, created = ReviewCategory.objects.get_or_create(
                    name=cat_data['name'],
                    platform=platform,
                    defaults={'is_active': True, 'display_order': 0}
                )
                
                CategoryRating.objects.get_or_create(
                    platform=platform,
                    category=category,
                    defaults={'rating': cat_data['rating']}
                )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully setup review platforms!')
        )
