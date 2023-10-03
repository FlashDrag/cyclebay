from django.urls import path

from . import views

urlpatterns = [
    path("", views.all_products, name="products"),
    path("featured/", views.featured_products, name="featured_products"),
    path("<int:product_id>/", views.product_detail, name="product_detail"),
]
