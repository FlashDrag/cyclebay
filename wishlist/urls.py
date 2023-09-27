from django.urls import path

from . import views

urlpatterns = [
    path("", views.wishlist, name="wishlist"),
    path(
        "add_to_wishlist_toggle/<int:product_id>/",
        views.add_to_wishlist_toggle,
        name="add_to_wishlist_toggle",
    ),
]
