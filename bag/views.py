from django.utils import timezone
from django.conf import settings
from cyclebay.celery import app as celery_app
from django.http import HttpResponse
from django.db import transaction
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages

from products.models import Product, ProductSize, Size
from .models import ProductReservation
from bag.tasks import release_reserving_products



def view_bag(request):
    """A view to return the bag contents page"""

    return render(request, "bag/bag.html")


def add_to_bag(request, item_id):
    """Add a product to the shopping bag"""

    product = get_object_or_404(Product, pk=item_id)
    size = request.POST.get("productsize")
    redirect_url = request.POST.get("redirect_url")

    # If the user selected a size, get the size object,
    # otherwise, return an error message and redirect
    try:
        size_obj = Size.objects.get(name__exact=size)
    except Size.DoesNotExist:
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

    # -- Celery --
    # Revoking the previous task, as new items have been added to the bag
    existing_task_id = request.session.get("clear_cart_task_id")
    if existing_task_id:
        celery_app.control.revoke(existing_task_id)
        del request.session["clear_cart_task_id"]

    # Schedule the new task and store its ID in the session
    countdown = int(settings.CART_EXPIRY_TIME) * 60
    task = release_reserving_products.apply_async(
        (request.session.session_key,), countdown=countdown
    )
    request.session["clear_cart_task_id"] = task.id
    # add the task expiry time to the session
    request.session["cart_expiration_time"] = (
        timezone.now() + timezone.timedelta(seconds=countdown)
    ).isoformat()
    request.session.modified = True

    return redirect(redirect_url)
