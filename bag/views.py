from cyclebay.celery import app as celery_app
from django.utils import timezone
from django.conf import settings
from django.http import HttpResponse, JsonResponse
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
            f"Updated <strong>{product_size_obj}</strong> quantity "
            f"to <strong>{bag[product_size_id]}</strong>",
            extra_tags="safe",
        )
    else:
        bag[product_size_id] = 1
        messages.success(
            request,
            f"Added <strong>{product_size_obj}</strong> to your cart",
            extra_tags="safe",
        )

    request.session["bag"] = bag

    # -- Celery --
    # Revoking the previous task, as new items have been added to the bag
    existing_task_id = request.session.get("clear_cart_task_id")
    if existing_task_id:
        celery_app.control.revoke(existing_task_id)
        del request.session["clear_cart_task_id"]

    # Schedule the new task and store its ID in the session
    countdown = int(settings.CART_EXPIRY_MINUTES) * 60
    task = release_reserving_products.apply_async(
        (request.session.session_key,), countdown=countdown
    )
    request.session["clear_cart_task_id"] = task.id
    # add the task expiry time to the session
    request.session["cart_expiration_time"] = (
        timezone.now() + timezone.timedelta(seconds=countdown)
    ).isoformat()
    # Set the expired message shown flag to False
    request.session["is_expired_msg_shown"] = False
    request.session.modified = True

    return redirect(redirect_url)


def remove_cart_expiration_time(request):
    """
    Remove the cart expiration time from the session
    to prevent the message from being shown again
    """
    request.session.pop("cart_expiration_time", None)

    return JsonResponse({"success": True})


def adjust_bag(request, product_size_id):
    """
    Adjust the quantity of the specified product_size to the specified amount
    """

    product_size_obj = get_object_or_404(ProductSize, pk=product_size_id)
    bag = request.session.get("bag", {})
    product_reservation = get_object_or_404(
        ProductReservation,
        product_size=product_size_obj,
        session_key=request.session.session_key,
    )

    quantity = int(request.POST.get("quantity"))

    if quantity > 0:
        bag[product_size_id] = quantity
        # If the quantity is greater than the number of available products,
        # raise an exception
        if quantity > (product_reservation.quantity + product_size_obj.count):
            raise Exception(
                "Quantity is greater than the number of available products"
            )
        # Reduce the product size object count by the difference between
        # the new quantity and the old quantity
        product_size_obj.count -= (quantity - product_reservation.quantity)
        product_size_obj.save()
        # Update the product reservation quantity
        product_reservation.quantity = quantity
        product_reservation.save()
        messages.success(
            request,
            f"Updated <strong>{product_size_obj}</strong> quantity"
            f" to <strong>{bag[product_size_id]}</strong>",
            extra_tags="safe",
        )
    else:
        # Remove the product size item from the bag
        bag.pop(product_size_id)
        # Increase the product size object count by the quantity
        # that was previously reserved
        product_size_obj.count += product_reservation.quantity
        product_size_obj.save()
        # Delete the product reservation
        product_reservation.delete()
        messages.success(
            request,
            f"Removed <strong>{product_size_obj}</strong> from your cart",  # noqa
            extra_tags="safe",
        )

    request.session["bag"] = bag

    return redirect(reverse("view_bag"))


def remove_from_bag(request, product_size_id):
    """Remove the product size item from the shopping bag and
    release the reserved products"""

    product_size_obj = get_object_or_404(ProductSize, pk=product_size_id)
    bag = request.session.get("bag", {})
    product_reservation = get_object_or_404(
        ProductReservation,
        product_size=product_size_obj,
        session_key=request.session.session_key,
    )

    # Remove the product size item from the bag
    bag.pop(product_size_id)
    # Increase the product size object count by the quantity
    # that was previously reserved
    product_size_obj.count += product_reservation.quantity
    product_size_obj.save()
    # Delete the product reservation
    product_reservation.delete()
    messages.success(
        request,
        f"Removed <strong>{product_size_obj}</strong> from your cart",  # noqa
        extra_tags="safe",
    )

    request.session["bag"] = bag

    # if bag is empty, remove the cart expiration time from the session,
    # to prevent the expired message from being shown
    if not bag:
        request.session.pop("cart_expiration_time", None)
        request.session.modified = True

    return HttpResponse(status=200)
