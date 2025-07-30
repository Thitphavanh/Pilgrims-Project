from django.core.management.base import BaseCommand
from django.utils.text import slugify
from restaurant.models import MenuItem  # Adjust import path based on your app name


class Command(BaseCommand):
    help = 'Load drinks menu data into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing drinks before loading new data',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be created without actually creating',
        )

    def handle(self, *args, **options):
        # Clear existing drinks if requested
        if options['clear']:
            deleted_count = MenuItem.objects.filter(category='drinks').count()
            if not options['dry_run']:
                MenuItem.objects.filter(category='drinks').delete()
            self.stdout.write(
                self.style.WARNING(f'{"Would delete" if options["dry_run"] else "Deleted"} {deleted_count} existing drinks')
            )

        # Cold Drinks Data
        cold_drinks = [
            {
                'name': 'Fresh Fruit Juice (Apple/Carrot/Ginger)',
                'description': 'Freshly squeezed fruit juice made with your choice of apple, carrot, or ginger. Rich in vitamins and natural flavors.',
                'price': 35000,
            },
            {
                'name': 'Fresh Squeezed Lemonade',
                'description': 'Refreshing lemonade made with fresh lemons, perfectly balanced sweet and tart flavor.',
                'price': 22000,
            },
            {
                'name': 'Fruit Ice + Sugar',
                'description': 'Traditional fruit ice drink sweetened with sugar, a perfect cool-down treat.',
                'price': 22000,
            },
            {
                'name': 'Fruit Smoothie',
                'description': 'Creamy and thick fruit smoothie blended with seasonal fresh fruits.',
                'price': 25000,
            },
            {
                'name': 'Yogurt + Ice + Sugar',
                'description': 'Refreshing yogurt drink blended with ice and sugar, light and creamy.',
                'price': 30000,
            },
            {
                'name': 'Iced Tea',
                'description': 'Classic iced tea served chilled, perfect for hot weather.',
                'price': 18000,
            },
            {
                'name': 'Iced Lemon Tea',
                'description': 'Refreshing iced tea infused with fresh lemon, citrusy and revitalizing.',
                'price': 22000,
            },
            {
                'name': 'Iced Honey Lemon Tea',
                'description': 'Iced tea with natural honey and fresh lemon, a healthy and tasty combination.',
                'price': 25000,
            },
            {
                'name': 'Iced Matcha Latte',
                'description': 'Premium Japanese matcha powder blended with milk and served over ice.',
                'price': 38000,
            },
            {
                'name': 'Milk Shake with Honey',
                'description': 'Creamy milkshake sweetened with natural honey, rich and satisfying.',
                'price': 32000,
            },
            {
                'name': 'Caramel Shake',
                'description': 'Indulgent milkshake with rich caramel flavor, sweet and creamy.',
                'price': 30000,
            },
            {
                'name': 'Iced Chocolate',
                'description': 'Cold chocolate drink, perfect for chocolate lovers on a hot day.',
                'price': 12000,
            },
            {
                'name': 'Soft Drinks',
                'description': 'Selection of carbonated soft drinks including Coca-Cola, Pepsi, Sprite, and more.',
                'price': 12000,
            },
            {
                'name': 'Orange / Apple Juice (Boxed)',
                'description': 'Premium boxed fruit juice, available in orange or apple flavor.',
                'price': 15000,
            },
            {
                'name': 'Glass of Wine Red/White',
                'description': 'Quality wine served by the glass, choice of red or white varieties.',
                'price': 45000,
            },
            {
                'name': 'Bottle of Wine',
                'description': 'Full bottle of wine, selection varies. Please ask our server for available options and pricing.',
                'price': 0,  # Price varies, ask server
            },
            {
                'name': 'Soda Water',
                'description': 'Plain carbonated water, refreshing and pure.',
                'price': 12000,
            },
            {
                'name': 'Mineral Water 500ml',
                'description': 'Pure mineral water in 500ml bottle, essential hydration.',
                'price': 7000,
            },
            {
                'name': 'Beer Lao White/Gold/Dark 330ml',
                'description': 'Local Beer Lao in 330ml bottle, available in White, Gold, or Dark varieties.',
                'price': 22000,
            },
            {
                'name': 'Beer Green',
                'description': 'Refreshing green beer, light and crisp flavor.',
                'price': 25000,
            },
            {
                'name': 'Somersby',
                'description': 'Apple cider with a fresh, fruity taste and natural apple flavor.',
                'price': 25000,
            },
        ]

        # Hot Drinks Data
        hot_drinks = [
            {
                'name': 'Chai Latte',
                'description': 'Spiced tea latte with aromatic spices and steamed milk, warming and comforting.',
                'price': 20000,
            },
            {
                'name': 'Masala Chai',
                'description': 'Traditional Indian spiced tea with a blend of aromatic spices and milk.',
                'price': 22000,
            },
            {
                'name': 'Hot Chocolate',
                'description': 'Rich and creamy hot chocolate, perfect for cold weather or chocolate cravings.',
                'price': 26000,
            },
            {
                'name': 'Hot Tea',
                'description': 'Classic hot tea, choose from our selection of premium tea blends.',
                'price': 18000,
            },
            {
                'name': 'Lemon Ginger Tea',
                'description': 'Warming tea infused with fresh lemon and ginger, great for digestion and immunity.',
                'price': 18000,
            },
            {
                'name': 'Honey Ginger Tea',
                'description': 'Soothing tea with natural honey and fresh ginger, perfect for wellness.',
                'price': 20000,
            },
            {
                'name': 'Matcha Tea',
                'description': 'Traditional Japanese green tea powder, earthy flavor with antioxidant benefits.',
                'price': 22000,
            },
            {
                'name': 'Matcha Latte',
                'description': 'Premium matcha powder blended with steamed milk, creamy and energizing.',
                'price': 30000,
            },
        ]

        # Combine all drinks
        all_drinks = []
        
        # Add cold drinks with subcategory
        for drink in cold_drinks:
            drink['subcategory'] = 'Cold Drinks'
            all_drinks.append(drink)
        
        # Add hot drinks with subcategory
        for drink in hot_drinks:
            drink['subcategory'] = 'Hot Drinks'
            all_drinks.append(drink)

        created_count = 0
        updated_count = 0
        skipped_count = 0

        for drink_data in all_drinks:
            # Create slug from name
            slug = slugify(drink_data['name'])
            
            # Check if item already exists
            existing_item = MenuItem.objects.filter(slug=slug).first()
            
            if existing_item:
                # Update existing item
                existing_item.description = drink_data['description']
                existing_item.price = drink_data['price']
                existing_item.category = 'drinks'
                
                if not options['dry_run']:
                    existing_item.save()
                    updated_count += 1
                    self.stdout.write(f'Updated: {drink_data["name"]}')
                else:
                    self.stdout.write(f'Would update: {drink_data["name"]}')
            else:
                # Create new item
                menu_item_data = {
                    'name': drink_data['name'],
                    'description': drink_data['description'],
                    'price': drink_data['price'],
                    'category': 'drinks',
                    'slug': slug,
                    'is_featured': False,  # Set to True for featured items if needed
                }
                
                if not options['dry_run']:
                    MenuItem.objects.create(**menu_item_data)
                    created_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'Created: {drink_data["name"]} - {drink_data["price"]} LAK')
                    )
                else:
                    self.stdout.write(f'Would create: {drink_data["name"]} - {drink_data["price"]} LAK')

        # Summary
        if options['dry_run']:
            self.stdout.write(
                self.style.WARNING(f'\nDRY RUN - No changes made to database')
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSummary:\n'
                f'Created: {created_count} items\n'
                f'Updated: {updated_count} items\n'
                f'Total drinks in menu: {len(all_drinks)}\n'
                f'Cold drinks: {len(cold_drinks)}\n'
                f'Hot drinks: {len(hot_drinks)}'
            )
        )

        # Show items that need manual price setting
        zero_price_items = [drink for drink in all_drinks if drink['price'] == 0]
        if zero_price_items:
            self.stdout.write(
                self.style.WARNING(
                    f'\nItems with variable pricing (need manual price setting):'
                )
            )
            for item in zero_price_items:
                self.stdout.write(f'- {item["name"]}')