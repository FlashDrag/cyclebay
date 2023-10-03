from django.shortcuts import render

from products.models import Product


def home(request):
    featured = Product.objects.filter(featured=True)[:8]

    context = {
        "featured": featured,
    }
    return render(request, "home/index.html", context)


def privacy(request):
    return render(request, "home/privacy.html")
