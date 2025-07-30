from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ("breakfast", "Breakfast"),
        ("coffee", "Coffee"),
        ("american", "American"),
        ("indian", "Indian"),
        ("drinks", "Drinks"),
        ("mexican", "Mexican"),
        ("pizza", "Pizza"),
        ("local_food", "Local Food"),
        ("soup_salad_mediterranean", "Soup, Salad & Mediterranean"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    is_featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to="menu_items/", null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.price} LAK"

    def get_absolute_url(self):
        """Get the canonical URL for this menu item"""
        return reverse("restaurant:menu_item_detail", kwargs={"slug": self.slug})

    def get_category_display_lao(self):
        """Get category display in Lao language"""
        category_lao = {
            "breakfast": "ອາຫານເຊົ້າ",
            "coffee": "ກາເຟ",
            "american": "ອາຫານອາເມຣິກາ",
            "indian": "ອາຫານອິນເດຍ",
            "drinks": "ເຄື່ອງດື່ມ",
            "mexican": "ອາຫານແມັກຊິໂກ",
            "pizza": "ພິຊຊ່າ",
            "local_food": "ອາຫານພື້ນເມືອງ",
            "soup_salad_mediterranean": "ແກງ & ສະຫຼັດ",
        }
        return category_lao.get(self.category, self.get_category_display())

    def save(self, *args, **kwargs):
        """Override save to ensure slug is created"""
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while MenuItem.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
