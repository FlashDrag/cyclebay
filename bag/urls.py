from django.urls import path

from . import views

urlpatterns = [
    path("", views.view_bag, name="view_bag"),
    path("add/<item_id>/", views.add_to_bag, name="add_to_bag"),
    path(
        "remove_cart_expiration_time/",
        views.remove_cart_expiration_time,
        name="remove_cart_expiration_time",
    ),
    path("adjust/<str:product_size_id>", views.adjust_bag, name="adjust_bag"),
    path(
        "remove/<str:product_size_id>",
        views.remove_from_bag,
        name="remove_from_bag",
    ),
]
