from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils.text import slugify


class CoffeeBean(models.Model):
    """ໂມເດວສຳລັບຂໍ້ມູນເມັດກາເຟ"""

    ORIGIN_CHOICES = [
        ("arabica", "ອາຣາບິກາ"),
        ("robusta", "ໂຣບັສຕາ"),
        ("liberica", "ລິເບຣິກາ"),
        ("excelsa", "ເອັກເຊວຊາ"),
    ]

    name = models.CharField(max_length=100)
    origin = models.CharField(max_length=20, choices=ORIGIN_CHOICES)
    country = models.CharField(max_length=50)
    region = models.CharField(max_length=100, blank=True)
    altitude = models.PositiveIntegerField(null=True, blank=True)
    flavor_notes = models.TextField(blank=True)
    acidity_level = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],
        default=3,
        verbose_name="ລະດັບຄວາມສົ້ມ (1-5)",
    )
    body_level = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)], default=3, verbose_name="ຄວາມເຂັ້ມຂຸ້ນ (1-5)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     verbose_name = 'ເມັດກາເຟ'
    #     verbose_name_plural = 'ເມັດກາເຟ'
    #     ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_origin_display()})"


class RoastLevel(models.Model):
    """ໂມເດວສຳລັບລະດັບການຄົ່ວ"""

    ROAST_CHOICES = [
        ("light", "ຄົ່ວອ່ອນ"),
        ("medium_light", "ຄົ່ວອ່ອນກາງ"),
        ("medium", "ຄົ່ວກາງ"),
        ("medium_dark", "ຄົ່ວເຂັ້ມກາງ"),
        ("dark", "ຄົ່ວເຂັ້ມ"),
        ("french", "ຄົ່ວແບບຝຣັ່ງ"),
        ("italian", "ຄົ່ວແບບອິຕາລີ"),
    ]

    name = models.CharField(max_length=20, choices=ROAST_CHOICES, unique=True)
    description = models.TextField(blank=True)
    temperature_range = models.CharField(max_length=50, blank=True)

    # class Meta:
    #     verbose_name = 'ລະດັບການຄົ່ວ'
    #     verbose_name_plural = 'ລະດັບການຄົ່ວ'

    def __str__(self):
        return self.get_name_display()


class CoffeeProduct(models.Model):
    """ໂມເດວສຳລັບຜະລິດຕະພັນກາເຟ"""

    GRIND_CHOICES = [
        ("whole_bean", "ເມັດເຕັມ"),
        ("coarse", "ບົດຫຍາບ"),
        ("medium_coarse", "ບົດກາງຫຍາບ"),
        ("medium", "ບົດກາງ"),
        ("medium_fine", "ບົດກາງລະອຽດ"),
        ("fine", "ບົດລະອຽດ"),
        ("extra_fine", "ບົດລະອຽດພິເສດ"),
    ]

    WEIGHT_UNIT_CHOICES = [
        ("g", "ກຣາມ"),
        ("kg", "ກິໂລກຣາມ"),
    ]
    name = models.CharField(max_length=100)
    images = models.ImageField(upload_to="products/")
    coffee_bean = models.ForeignKey(CoffeeBean, on_delete=models.CASCADE)
    roast_level = models.ForeignKey(RoastLevel, on_delete=models.CASCADE)
    grind_type = models.CharField(
        max_length=20, choices=GRIND_CHOICES, default="whole_bean"
    )
    # ຂໍ້ມູນນ້ຳໜັກແລະລາຄາ
    weight = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    weight_unit = models.CharField(
        max_length=5, choices=WEIGHT_UNIT_CHOICES, default="g"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    # ຂໍ້ມູນເພີ່ມເຕີມ
    description = models.TextField(blank=True)
    brewing_method = models.CharField(max_length=100, blank=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    # ວັນທີ
    roast_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return f"{self.name} - {self.weight}{self.weight_unit}"

    def save(self, *args, **kwargs):
        """Override save to ensure slug is created"""
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while CoffeeProduct.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def price_per_unit(self):
        """ຄຳນວນລາຄາຕໍ່ໜ່ວຍນ້ຳໜັກ"""
        if self.weight_unit == "kg":
            weight_in_grams = self.weight * 1000
        else:
            weight_in_grams = self.weight

        return round(self.price / weight_in_grams * 100, 2)  # ລາຄາຕໍ່ 100 ກຣາມ

    @property
    def is_fresh(self):
        """ກວດສອບຄວາມສົດຂອງກາເຟ (ພາຍໃນ 30 ມື້)"""
        if not self.roast_date:
            return None

        from datetime import date, timedelta

        return (date.today() - self.roast_date).days <= 30


class ProductImage(models.Model):
    product = models.ForeignKey(
        CoffeeProduct, related_name="gallery_images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="products/")
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} - Image"


class CoffeeCategory(models.Model):
    """ໂມເດວສຳລັບໝວດໝູ່ກາເຟ"""

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)

    # class Meta:
    #     verbose_name = 'ໝວດໝູ່ກາເຟ'
    #     verbose_name_plural = 'ໝວດໝູ່ກາເຟ'
    #     ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("category_detail", kwargs={"slug": self.slug})


# ເພີ່ມ Many-to-Many relationship
CoffeeProduct.add_to_class(
    "categories", models.ManyToManyField(CoffeeCategory, blank=True)
)


class CoffeeReview(models.Model):
    """ໂມເດວສຳລັບການຣີວິວກາເຟ"""

    coffee_product = models.ForeignKey(
        CoffeeProduct, on_delete=models.CASCADE, related_name="reviews"
    )
    reviewer_name = models.CharField(max_length=100)
    rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)], verbose_name="ຄະແນນ (1-5 ດາວ)"
    )
    comment = models.TextField(verbose_name="ຄຳເຫັນ")
    created_at = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     verbose_name = 'ການຣີວິວກາເຟ'
    #     verbose_name_plural = 'ການຣີວິວກາເຟ'
    #     ordering = ['-created_at']

    def __str__(self):
        return f"{self.coffee_product.name} - {self.rating} ດາວ"
