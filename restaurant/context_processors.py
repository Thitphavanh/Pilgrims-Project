from .models import MenuCategory, MenuItem

def menu_categories(request):
    categories = MenuCategory.objects.all().order_by('name')
    menu_data = []
    for category in categories:
        items = MenuItem.objects.filter(category=category).order_by('name')
        menu_data.append({
            'category': category,
            'items': items
        })
    return {
        'menu_data': menu_data
    }
