# coffee/management/commands/seed_coffee_data.py

from django.core.management.base import BaseCommand
from coffee.models import CoffeeBean, RoastLevel, CoffeeProduct, CoffeeCategory
from datetime import date, timedelta
from decimal import Decimal

class Command(BaseCommand):
    help = 'Seeds the database with 10 coffee product records for testing.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing coffee data before adding new ones',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Deleting existing coffee data...'))
            CoffeeProduct.objects.all().delete()
            CoffeeBean.objects.all().delete()
            RoastLevel.objects.all().delete()
            CoffeeCategory.objects.all().delete()

        self.stdout.write('Creating coffee data...')

        # Create roast levels
        roast_levels_data = [
            ('light', 'Light roast with bright acidity and floral notes', '180-205°C'),
            ('medium', 'Balanced roast with moderate acidity and body', '210-220°C'),
            ('medium_dark', 'Rich roast with bold flavor and reduced acidity', '225-230°C'),
            ('dark', 'Full-bodied roast with intense flavor', '240-250°C'),
        ]

        roast_levels = {}
        for name, desc, temp in roast_levels_data:
            roast_level, created = RoastLevel.objects.get_or_create(
                name=name,
                defaults={'description': desc, 'temperature_range': temp}
            )
            roast_levels[name] = roast_level
            if created:
                self.stdout.write(f'  - Created roast level: {roast_level}')

        # Create coffee categories
        categories_data = [
            ('Single Origin', 'Coffee from a single farm or region'),
            ('Blends', 'Carefully crafted coffee blends'),
            ('Specialty', 'Premium and rare coffee varieties'),
        ]

        categories = {}
        for name, desc in categories_data:
            category, created = CoffeeCategory.objects.get_or_create(
                name=name,
                defaults={'description': desc}
            )
            categories[name] = category
            if created:
                self.stdout.write(f'  - Created category: {category}')

        # Create coffee beans
        beans_data = [
            ('Ethiopian Yirgacheffe', 'arabica', 'Ethiopia', 'Yirgacheffe', 1900, 'Floral, citrusy, tea-like', 5, 3),
            ('Colombian Supremo', 'arabica', 'Colombia', 'Huila', 1600, 'Nutty, chocolatey, caramel', 4, 4),
            ('Brazilian Santos', 'arabica', 'Brazil', 'Santos', 1100, 'Smooth, nutty, low acidity', 2, 4),
            ('Vietnamese Robusta', 'robusta', 'Vietnam', 'Da Lat', 1500, 'Strong, earthy, bitter', 2, 5),
            ('Jamaican Blue Mountain', 'arabica', 'Jamaica', 'Blue Mountain', 2000, 'Mild, balanced, refined', 3, 3),
            ('Kenyan AA', 'arabica', 'Kenya', 'Central Province', 1700, 'Wine-like, blackcurrant, bright', 5, 4),
            ('Hawaiian Kona', 'arabica', 'USA', 'Hawaii', 800, 'Smooth, rich, low acidity', 3, 3),
            ('Guatemalan Antigua', 'arabica', 'Guatemala', 'Antigua', 1500, 'Spicy, smoky, full-bodied', 4, 4),
        ]

        beans = {}
        for name, origin, country, region, alt, flavor, acid, body in beans_data:
            bean, created = CoffeeBean.objects.get_or_create(
                name=name,
                defaults={
                    'origin': origin,
                    'country': country,
                    'region': region,
                    'altitude': alt,
                    'flavor_notes': flavor,
                    'acidity_level': acid,
                    'body_level': body
                }
            )
            beans[name] = bean
            if created:
                self.stdout.write(f'  - Created bean: {bean}')

        # Create 10 coffee products
        products_data = [
            {
                'name': 'Ethiopian Yirgacheffe Light Roast',
                'bean': 'Ethiopian Yirgacheffe',
                'roast': 'light',
                'grind_type': 'whole_bean',
                'weight': Decimal('250'),
                'price': Decimal('45000'),
                'description': 'Bright and floral Ethiopian coffee with citrus notes',
                'brewing_method': 'Pour over, V60',
                'stock_quantity': 50,
                'categories': ['Single Origin', 'Specialty']
            },
            {
                'name': 'Colombian Supremo Medium Roast',
                'bean': 'Colombian Supremo',
                'roast': 'medium',
                'grind_type': 'medium',
                'weight': Decimal('500'),
                'price': Decimal('65000'),
                'description': 'Classic Colombian coffee with chocolate and caramel notes',
                'brewing_method': 'French press, Drip',
                'stock_quantity':75,
                'categories': ['Single Origin']
            },
            {
                'name': 'Brazilian Santos Dark Roast',
                'bean': 'Brazilian Santos',
                'roast': 'dark',
                'grind_type': 'coarse',
                'weight': Decimal('1'),
                'weight_unit': 'kg',
                'price': Decimal('85000'),
                'description': 'Smooth Brazilian coffee perfect for espresso',
                'brewing_method': 'Espresso, Moka pot',
                'stock_quantity':30,
                'categories': ['Blends']
            },
            {
                'name': 'Vietnamese Robusta Strong Blend',
                'bean': 'Vietnamese Robusta',
                'roast': 'dark',
                'grind_type': 'fine',
                'weight': Decimal('250'),
                'price': Decimal('35000'),
                'description': 'Strong and bold Vietnamese coffee',
                'brewing_method': 'Vietnamese drip, Espresso',
                'stock_quantity':40,
                'categories': ['Blends']
            },
            {
                'name': 'Jamaican Blue Mountain Premium',
                'bean': 'Jamaican Blue Mountain',
                'roast': 'medium',
                'grind_type': 'whole_bean',
                'weight': Decimal('125'),
                'price': Decimal('120000'),
                'description': 'Rare and exquisite Jamaican coffee',
                'brewing_method': 'Pour over, French press',
                'stock_quantity':15,
                'categories': ['Specialty']
            },
            {
                'name': 'Kenyan AA Bright Roast',
                'bean': 'Kenyan AA',
                'roast': 'light',
                'grind_type': 'medium_fine',
                'weight': Decimal('250'),
                'price': Decimal('55000'),
                'description': 'Bright Kenyan coffee with wine-like characteristics',
                'brewing_method': 'Chemex, V60',
                'stock_quantity':60,
                'categories': ['Single Origin']
            },
            {
                'name': 'Hawaiian Kona Smooth',
                'bean': 'Hawaiian Kona',
                'roast': 'medium',
                'grind_type': 'whole_bean',
                'weight': Decimal('200'),
                'price': Decimal('95000'),
                'description': 'Smooth and rich Hawaiian coffee',
                'brewing_method': 'Drip, French press',
                'stock_quantity':25,
                'categories': ['Specialty']
            },
            {
                'name': 'Guatemalan Antigua Smoky',
                'bean': 'Guatemalan Antigua',
                'roast': 'medium_dark',
                'grind_type': 'coarse',
                'weight': Decimal('500'),
                'price': Decimal('70000'),
                'description': 'Full-bodied Guatemalan coffee with smoky notes',
                'brewing_method': 'French press, Cold brew',
                'stock_quantity':45,
                'categories': ['Single Origin']
            },
            {
                'name': 'House Blend Medium Roast',
                'bean': 'Colombian Supremo',
                'roast': 'medium',
                'grind_type': 'medium',
                'weight': Decimal('1'),
                'weight_unit': 'kg',
                'price': Decimal('75000'),
                'description': 'Our signature house blend for everyday enjoyment',
                'brewing_method': 'Drip, French press',
                'stock_quantity':100,
                'categories': ['Blends']
            },
            {
                'name': 'Espresso Blend Dark',
                'bean': 'Brazilian Santos',
                'roast': 'dark',
                'grind_type': 'fine',
                'weight': Decimal('250'),
                'price': Decimal('42000'),
                'description': 'Perfect espresso blend with rich crema',
                'brewing_method': 'Espresso machine',
                'stock_quantity':80,
                'categories': ['Blends']
            },
        ]

        created_count = 0
        roast_date = date.today() - timedelta(days=7)  # Roasted a week ago

        for product_data in products_data:
            # Extract categories for later
            category_names = product_data.pop('categories', [])

            # Get the bean and roast level
            bean = beans[product_data.pop('bean')]
            roast_level = roast_levels[product_data.pop('roast')]

            # Create the product
            product, created = CoffeeProduct.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    **product_data,
                    'coffee_bean': bean,
                    'roast_level': roast_level,
                    'weight_unit': product_data.get('weight_unit', 'g'),
                    'stock_quantity': product_data.pop('stock_quantity'),
                    'roast_date': roast_date,
                    'expiry_date': roast_date + timedelta(days=365),
                }
            )

            if created:
                # Add categories
                for cat_name in category_names:
                    if cat_name in categories:
                        product.categories.add(categories[cat_name])

                created_count += 1
                self.stdout.write(f'  - Created product: {product.name} - {product.price} LAK')
            else:
                self.stdout.write(f'  - Skipped product: {product.name} (already exists)')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} coffee products. '
                f'Total products in database: {CoffeeProduct.objects.count()}'
            )
        )