from django.contrib import admin
from .models import Category, Brand, Size, Colour, Product, ProductSize


class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1  # how many rows to show


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = ProductSizeInline,

    list_display = (
        "category",
        "brand",
        "name",
        "price",
        "colour",
        "featured",
        "image",
    )
    list_filter = (
        "category",
        "brand",
        "colour",
        "featured",
    )
    search_fields = (
        "name",
        "brand__name",
        "category__name",
        "colour__name",
        "sku",
    )

    ordering = (
        "category",
        "brand",
        "name",
        "price",
        "colour",
        "featured",
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "friendly_name",
        "name",
    )
    search_fields = (
        "name",
        "friendly_name",
    )


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = (
        "friendly_name",
        "name",
    )
    search_fields = (
        "name",
        "friendly_name",
    )


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = (
        "friendly_name",
        "name",
    )
    search_fields = (
        "name",
        "friendly_name",
    )


@admin.register(Colour)
class ColourAdmin(admin.ModelAdmin):
    list_display = (
        "friendly_name",
        "name",
    )
    search_fields = (
        "name",
        "friendly_name",
    )
