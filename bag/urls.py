from django.urls import path

from . import views

urlpatterns = [
    path("add/<item_id>/", views.add_to_bag, name="add_to_bag"),
]
