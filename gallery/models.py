
from django.db import models
from django.utils.text import slugify

class GalleryCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Name in English")
    name_lo = models.CharField(max_length=100, blank=True, help_text="Name in Lao")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    image = models.ImageField(upload_to='gallery_categories/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_localized_name(self, language_code='en'):
        """Return the name in the requested language"""
        if language_code == 'lo' and self.name_lo:
            return self.name_lo
        return self.name

    def __str__(self):
        return self.name

class GalleryImage(models.Model):
    category = models.ForeignKey(GalleryCategory, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery/')
    title = models.CharField(max_length=200, blank=True, help_text="Title in English")
    title_lo = models.CharField(max_length=200, blank=True, help_text="Title in Lao")
    description = models.TextField(blank=True, help_text="Description in English")
    description_lo = models.TextField(blank=True, help_text="Description in Lao")

    def get_localized_title(self, language_code='en'):
        """Return the title in the requested language"""
        if language_code == 'lo' and self.title_lo:
            return self.title_lo
        return self.title

    def get_localized_description(self, language_code='en'):
        """Return the description in the requested language"""
        if language_code == 'lo' and self.description_lo:
            return self.description_lo
        return self.description

    def __str__(self):
        return self.title or f"Image in {self.category.name}"
