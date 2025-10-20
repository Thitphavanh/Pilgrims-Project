from django.db import models
from django.utils.translation import gettext_lazy as _

class HeroSlide(models.Model):
    image = models.ImageField(_("Image"), upload_to='hero_slides/')
    caption = models.CharField(_("Caption"), max_length=255, blank=True, null=True)
    link_url = models.URLField(_("Link URL"), max_length=200, blank=True, null=True)
    order = models.IntegerField(_("Order"), default=0, help_text=_("Order in which the slide appears"))
    is_active = models.BooleanField(_("Is Active"), default=True)

    class Meta:
        verbose_name = _("Hero Slide")
        verbose_name_plural = _("Hero Slides")
        ordering = ['order']

    def __str__(self):
        return f"Slide {self.order}: {self.caption or self.image.name}"


class Gallery(models.Model):
    """Gallery model for storing images with categories"""

    CATEGORY_CHOICES = [
        ('savannakhet', _('Savannakhet')),
        ('hotel', _('Hotel')),
        ('restaurant', _('Restaurant')),
        ('food', _('Food')),
        ('outside_sitting', _('Outside Sitting')),
        ('coffee', _('Coffee')),
    ]

    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"), blank=True, null=True)
    image = models.ImageField(_("Image"), upload_to='gallery/')
    category = models.CharField(
        _("Category"),
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='savannakhet'
    )
    order = models.IntegerField(_("Order"), default=0, help_text=_("Order in which the image appears"))
    is_active = models.BooleanField(_("Is Active"), default=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Gallery Image")
        verbose_name_plural = _("Gallery Images")
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.get_category_display()}"


class VisitorCount(models.Model):
    """Model to track website visitor count"""

    count = models.PositiveIntegerField(_("Visitor Count"), default=0)
    last_updated = models.DateTimeField(_("Last Updated"), auto_now=True)

    class Meta:
        verbose_name = _("Visitor Count")
        verbose_name_plural = _("Visitor Counts")

    def __str__(self):
        return f"Total Visitors: {self.count}"

    @classmethod
    def increment(cls):
        """Increment visitor count"""
        obj, created = cls.objects.get_or_create(id=1)
        obj.count += 1
        obj.save()
        return obj.count

    @classmethod
    def get_count(cls):
        """Get current visitor count"""
        obj, created = cls.objects.get_or_create(id=1)
        return obj.count
