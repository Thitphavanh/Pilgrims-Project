from django.core.management.base import BaseCommand
from django.utils.text import slugify
from hotel.models import Room


class Command(BaseCommand):
    help = "Generate slugs for existing rooms"

    def handle(self, *args, **options):
        self.stdout.write("Generating slugs for rooms...")

        rooms = Room.objects.filter(slug__isnull=True)
        updated_count = 0

        for room in rooms:
            if room.room_type:
                base_slug = slugify(f"{room.room_type.name}")
                slug = f"{base_slug}-{room.id}"
                counter = 1

                # Ensure uniqueness
                while Room.objects.filter(slug=slug).exclude(pk=room.pk).exists():
                    slug = f"{base_slug}-{room.id}-{counter}"
                    counter += 1

                room.slug = slug
                room.save()
                updated_count += 1

                self.stdout.write(
                    f"Room {room.id} ({room.room_type.name}) -> slug: {slug}"
                )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully generated slugs for {updated_count} rooms")
        )