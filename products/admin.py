from django.contrib import admin
from .models import Category, Brand, Size, Color, Product, ProductSize


class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1  # how many rows to show

    ordering = ("size",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = ProductSizeInline,

    list_display = (
        "category",
        "brand",
        "name",
        "price",
        "color",
        "sku",
        "featured",
        "image",
    )
    list_filter = (
        "category",
        "brand",
        "color",
        "sizes",
        "featured",
    )
    search_fields = (
        "name",
        "brand__name",
        "category__name",
        "color__name",
        "sku",
    )

    ordering = ("sku",)


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


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = (
        "friendly_name",
        "name",
    )
    search_fields = (
        "name",
        "friendly_name",
    )
