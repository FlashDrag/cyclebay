from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q

from .models import Brand, Category, Color, Product


def all_products(request):
    """All products, including sorting and search queries"""
    products = Product.objects.all()
    query = None
    categories = None
    brands = None
    colors = None
    sort = None
    direction = None

    if request.GET:
        # TODO: add sorting

        if "category" in request.GET:
            # get category string value and split it into a list
            categories = request.GET["category"].split(",")
            # exact case insensitive match for category name
            cat_query = Q()
            for category in categories:
                cat_query |= Q(name__iexact=category.strip())
            categories = Category.objects.filter(cat_query)
            # filter products by category
            products = products.filter(category__in=categories)

        if "brand" in request.GET:
            brands = request.GET["brand"].split(",")
            br_query = Q()
            for brand in brands:
                br_query |= Q(name__iexact=brand.strip())
            brands = Brand.objects.filter(br_query)
            products = products.filter(brand__in=brands)

        if "color" in request.GET:
            colors = request.GET["color"].split(",")
            col_query = Q()
            for color in colors:
                col_query |= Q(name__iexact=color.strip())
            colors = Color.objects.filter(col_query)
            products = products.filter(color__in=colors)

        if "q" in request.GET:
            # get the search query
            query = request.GET["q"]
            if not query.strip():
                messages.error(
                    request, "You didn't enter any search criteria!"
                )
                return redirect(reverse("products"))
            # look for the query in the product name or brand name
            queries = (
                Q(name__icontains=query)
                | Q(brand__name__icontains=query)
            )
            products = products.filter(queries)

    current_sorting = f"{sort}_{direction}"

    context = {
        "products": products,
        "search_term": query,
        "current_categories": categories,
        "current_brands": brands,
        "current_colors": colors,
        "current_sorting": current_sorting,
    }
    return render(request, "products/products.html", context)


def product_detail(request, product_id):
    """Individual product details"""
    product = get_object_or_404(Product, pk=product_id)
    context = {
        "product": product,
    }
    return render(request, "products/product_detail.html", context)
