from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import MenuItem


@receiver(pre_save, sender=MenuItem)
def create_menu_item_slug(sender, instance, **kwargs):
    """
    Automatically create a unique slug for menu items
    """
    if not instance.slug:
        # Create base slug from name
        base_slug = slugify(instance.name)
        slug = base_slug

        # Check if slug already exists and make it unique
        counter = 1
        while MenuItem.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        instance.slug = slug
