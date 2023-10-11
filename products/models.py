from re import match
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

from cyclebay.models import TimeStampModel


class Category(models.Model):
    name = models.CharField(max_length=254, unique=True)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Brand(models.Model):
    name = models.CharField(max_length=254, unique=True)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Size(models.Model):
    name = models.CharField(max_length=50, unique=True)
    friendly_name = models.CharField(max_length=50, null=True, blank=True)
    order = models.PositiveIntegerField(unique=True)

    def __str__(self) -> str:
        return self.name

    def get_friendly_name(self):
        return self.friendly_name

    class Meta:
        ordering = ["order"]


def validate_color(value):
    """Validate the new color name if it is in hex format"""
    # match both shorthand HEX colors #RGB and full HEX colors #RRGGBB.
    regex = r"^#(?:[0-9a-fA-F]{3}){1,2}$"
    if not match(regex, value):
        raise ValidationError("Please enter a valid HEX color code!")


class Color(models.Model):
    # color name is the HEX color code
    name = models.CharField(
        max_length=7, unique=True, validators=[validate_color]
    )
    friendly_name = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(TimeStampModel):
    category = models.ForeignKey(
        "Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="products",
    )
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    brand = models.ForeignKey(
        Brand,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="products",
    )
    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        )
    sizes = models.ManyToManyField(
        Size,
        # specify the intermediate model that will be used
        # to link the two models together
        through="ProductSize",
        related_name="products",
    )
    color = models.ForeignKey(
        Color,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="products",
    )
    featured = models.BooleanField(default=False)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def total_count(self):
        """Return the total count of all sizes of a product"""
        return ProductSize.objects.filter(product=self).aggregate(
            total=models.Sum("count")
        )["total"]


class ProductSize(models.Model):
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(999)]
    )

    class Meta:
        # ensure that the combination of size and product is unique
        unique_together = ("size", "product")
        ordering = ["size"]

    def __str__(self) -> str:
        return f"{self.product.name} - {self.size.name}"
