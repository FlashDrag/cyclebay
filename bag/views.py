from django.http import HttpResponse
from django.db import transaction
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages

from .models import ProductReservation
from products.models import Product, ProductSize, Size


def view_bag(request):
    """A view to return the bag contents page"""

    return render(request, "bag/bag.html")


def add_to_bag(request, item_id):
    """Add a product to the shopping bag"""

    product = get_object_or_404(Product, pk=item_id)
    size_list = request.POST.get("productsize")
    redirect_url = request.POST.get("redirect_url")

    # If the user selected a size, get the size object,
    # otherwise, return an error message and redirect
    size_obj = Size.objects.filter(name__in=size_list).first()
    if len(size_list) != 1 or not size_obj:
        messages.error(request, f"Please select a size for {product.name}")
        return redirect(redirect_url)

    # Get the product size object associated with the product and size
    product_size_obj = get_object_or_404(
        ProductSize, size=size_obj, product=product
    )
    product_size_id = str(product_size_obj.id)

    # If the product size object is out of stock, return an error message
    if product_size_obj.count < 1:
        messages.error(
            request,
            f"Sorry, {product_size_obj} is out of stock. "
            "Please try again later.",
        )
        return redirect(redirect_url)

    # transaction.atomic() ensures that the database changes are
    # only committed if all the operations succeed
    with transaction.atomic():
        # Reduce the product size object count by 1 and save it
        product_size_obj.count -= 1
        product_size_obj.save()

        # Create a product reservation object for the product size
        reservation, created = ProductReservation.objects.get_or_create(
            product_size=product_size_obj,
            session_key=request.session.session_key,
            defaults={"quantity": 0},
        )
        reservation.quantity += 1
        reservation.save()

    bag = request.session.get("bag", {})

    if product_size_id in list(bag.keys()):
        bag[product_size_id] += 1
        messages.success(
            request,
            f"Updated {product_size_obj} quantity to {bag[product_size_id]}",
        )
    else:
        bag[product_size_id] = 1
        messages.success(request, f"Added {product_size_obj} to your bag")

    request.session["bag"] = bag

    return redirect(redirect_url)
