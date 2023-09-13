from django.shortcuts import render
from .models import Product


def all_products(request):
    """ All products, including sorting and search queries"""
    bikes = Product.objects.all()
    context = {
        "products": bikes,
    }
    return render(request, "products/products.html", context)
