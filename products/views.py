from django.shortcuts import get_object_or_404, render
from .models import Product


def all_products(request):
    """ All products, including sorting and search queries"""
    bikes = Product.objects.all()
    context = {
        "products": bikes,
    }
    return render(request, "products/products.html", context)


def product_detail(request, product_id):
    """ Individual product details """
    product = get_object_or_404(Product, pk=product_id)
    context = {
        "product": product,
    }
    return render(request, "products/product_detail.html", context)
