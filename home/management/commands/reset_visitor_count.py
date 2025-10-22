from django.core.management.base import BaseCommand
from home.models import VisitorCount


class Command(BaseCommand):
    help = 'Reset visitor count to zero'

    def handle(self, *args, **options):
        try:
            visitor_count = VisitorCount.objects.get(id=1)
            old_count = visitor_count.count
            visitor_count.count = 0
            visitor_count.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully reset visitor count from {old_count:,} to 0'
                )
            )
        except VisitorCount.DoesNotExist:
            # Create a new visitor count if it doesn't exist
            VisitorCount.objects.create(id=1, count=0)
            self.stdout.write(
                self.style.SUCCESS(
                    'Created new visitor count record initialized to 0'
                )
            )
