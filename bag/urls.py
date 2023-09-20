from django.urls import path

from . import views

urlpatterns = [
    path("", views.view_bag, name="view_bag"),
    path("add/<item_id>/", views.add_to_bag, name="add_to_bag"),
    path(
        "set_expired_msg_shown/",
        views.set_expired_msg_shown,
        name="set_expired_msg_shown",
    ),
    path("adjust/<str:product_size_id>", views.adjust_bag, name="adjust_bag"),
]
