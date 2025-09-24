# coffee/management/commands/generate_coffee_slugs.py

from django.core.management.base import BaseCommand
from coffee.models import CoffeeProduct

class Command(BaseCommand):
    help = 'Generates slugs for existing coffee products that do not have slugs.'

    def handle(self, *args, **options):
        products_without_slugs = CoffeeProduct.objects.filter(slug__isnull=True)

        if not products_without_slugs.exists():
            self.stdout.write(
                self.style.SUCCESS('All coffee products already have slugs.')
            )
            return

        self.stdout.write(f'Found {products_without_slugs.count()} products without slugs.')

        updated_count = 0
        for product in products_without_slugs:
            old_slug = product.slug
            product.save()  # This will trigger slug generation in the save method
            updated_count += 1
            self.stdout.write(f'  - Generated slug for "{product.name}": {product.slug}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully generated slugs for {updated_count} coffee products.'
            )
        )