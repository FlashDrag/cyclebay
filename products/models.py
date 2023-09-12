from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    class Size(models.TextChoices):
        XSMALL = "XS", "Extra Small"
        SMALL = "S", "Small"
        MEDIUM = "M", "Medium"
        LARGE = "L", "Large"
        XLARGE = "X", "XLarge"
        OTHER = "O", "Other"

    class Brand(models.TextChoices):
        AXESS = "AX", "Axess"
        CICLISTA = "CI", "Ciclista"
        CUBE = "CU", "Cube"
        KTM = "KT", "KTM"
        OTHER = "O", "Other"

    class Colour(models.TextChoices):
        BLACK_GREY = "BG", "black/grey"
        GREEN = "GR", "green"
        WHITE = "WH", "white"
        BLUE = "BL", "blue"
        BRAUN = "BR", "braun"
        RED_ORANGE = "RO", "red/orange"
        YELLOW = "YE", "yellow"
        OTHER = "O", "Other"

    category = models.ForeignKey(
        "Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="products",
    )
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    brand = models.CharField(
        max_length=2,
        choices=Brand.choices,
        default=Brand.OTHER,
    )
    price = models.DecimalField(max_digits=7, decimal_places=2)
    size = models.CharField(
        max_length=2,
        choices=Size.choices,
        default=Size.OTHER,
    )
    colour = models.CharField(
        max_length=2,
        choices=Colour.choices,
        default=Colour.OTHER,
    )
    featured = models.BooleanField(default=False)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name
