
from django.db import models
from django.utils.text import slugify

class GalleryCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    image = models.ImageField(upload_to='gallery_categories/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class GalleryImage(models.Model):
    category = models.ForeignKey(GalleryCategory, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery/')
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title or f"Image in {self.category.name}"
