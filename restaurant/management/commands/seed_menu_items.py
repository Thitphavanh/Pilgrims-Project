# restaurant/management/commands/seed_menu_items.py

from django.core.management.base import BaseCommand
from restaurant.models import MenuItem

MENU_ITEMS = [
    {
        "name": "Lao Style Omelette (Khai Jiao)",
        "description": "A fluffy omelette with herbs, served with steamed rice. A simple yet classic Lao breakfast.",
        "price": 35000,
        "category": "breakfast",
        "is_featured": True,
    },
    {
        "name": "Iced Cappuccino",
        "description": "Rich espresso with steamed milk foam, served over ice for a refreshing kick.",
        "price": 28000,
        "category": "coffee",
        "is_featured": False,
    },
    {
        "name": "Classic Beef Burger",
        "description": "Juicy grilled beef patty, cheddar cheese, lettuce, tomato, and our special sauce in a toasted bun.",
        "price": 75000,
        "category": "american",
        "is_featured": True,
    },
    {
        "name": "Chicken Tikka Masala",
        "description": "Tender chicken pieces in a creamy, spiced tomato sauce. Served with naan bread.",
        "price": 85000,
        "category": "indian",
        "is_featured": False,
    },
    {
        "name": "Mango Sticky Rice Shake",
        "description": "A delicious blend of sweet mango, sticky rice, and coconut milk. A dessert and drink in one!",
        "price": 30000,
        "category": "drinks",
        "is_featured": True,
    },
    {
        "name": "Margherita Pizza",
        "description": "Classic Italian pizza with a rich tomato sauce, fresh mozzarella, and basil leaves.",
        "price": 90000,
        "category": "pizza",
        "is_featured": False,
    },
    {
        "name": "Lao Sausage (Sai Oua)",
        "description": "Famous local pork sausage, seasoned with lemongrass, galangal, kaffir lime leaves, and chili. A must-try!",
        "price": 60000,
        "category": "local_food",
        "is_featured": True,
    },
    {
        "name": "Green Papaya Salad (Tam Mak Hoong)",
        "description": "Spicy and sour green papaya salad with tomatoes, chili, lime, and fish sauce.",
        "price": 40000,
        "category": "soup_salad_mediterranean",
        "is_featured": False,
    },
    {
        "name": "Laap Ped (Spicy Duck Salad)",
        "description": "A traditional Lao minced duck salad with fresh herbs, roasted ground rice, and chili.",
        "price": 70000,
        "category": "local_food",
        "is_featured": True,
    },
    {
        "name": "Beerlao",
        "description": "The national beer of Laos, a crisp and refreshing lager.",
        "price": 18000,
        "category": "drinks",
        "is_featured": False,
    },
]

class Command(BaseCommand):
    help = 'Seeds the database with initial menu items for the restaurant.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Deleting all existing menu items...'))
        MenuItem.objects.all().delete()
        
        self.stdout.write('Creating new menu items...')
        for item_data in MENU_ITEMS:
            item = MenuItem.objects.create(**item_data)
            self.stdout.write(f'  - Created "{item.name}"')
            
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database with menu items.'))