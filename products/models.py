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


class Brand(models.Model):
    name = models.CharField(max_length=254, unique=True)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Size(models.Model):
    name = models.CharField(max_length=50, unique=True)
    friendly_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Colour(models.Model):
    name = models.CharField(max_length=50, unique=True)
    friendly_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
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
    price = models.DecimalField(max_digits=7, decimal_places=2)
    sizes = models.ManyToManyField(
        Size,
        # specify the intermediate model that will be used
        # to link the two models together
        through="ProductSize",
        related_name="products",
    )
    colour = models.ForeignKey(
        Colour,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="products",
    )
    featured = models.BooleanField(default=False)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class ProductSize(models.Model):
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)

    class Meta:
        # ensure that the combination of size and product is unique
        unique_together = ("size", "product")

    def __str__(self) -> str:
        return f"{self.product.name} - {self.size.name}"
