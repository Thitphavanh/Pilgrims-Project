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
