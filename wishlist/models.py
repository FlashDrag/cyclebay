from django.db import models
from products.models import Product
from profiles.models import UserProfile


class Wishlist(models.Model):
    """
    A Wishlist model for maintaining a list of favorite products
    """
    # ensures that each user can only have one wishlist
    user_profile = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='wishlist'
    )
    # User can add many products to their wishlist,
    # and each product can be added to many wishlists
    products = models.ManyToManyField(
        Product,
        related_name='wishlists',
    )

    def __str__(self):
        return self.user_profile.user.email
