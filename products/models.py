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
