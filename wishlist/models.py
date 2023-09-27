from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
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


@receiver(post_save, sender=UserProfile)
def create_wishlist(sender, instance, created, **kwargs):
    """
    Create a wishlist for each new user using the post_save signal
    """
    if created:
        Wishlist.objects.create(user_profile=instance)
