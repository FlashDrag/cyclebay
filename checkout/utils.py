from cyclebay.celery import app as celery_app
from django.utils import timezone
from django.conf import settings
from django.db import transaction

from .models import ProductReservation
from .tasks import release_reserving_products


@transaction.atomic
def reserve_products(current_bag, request):
    bag_items = current_bag.get("bag_items")
    session_key = request.session.session_key

    for item in bag_items:
        product_size_id = item['product_size_id']
        product_size_obj = item['product_size_obj']
        quantity = item['quantity']

        # Decrease the product size object count by the quantity
        product_size_obj.count -= quantity
        product_size_obj.save()

        # Create or update the product reservation
        reservation, created = ProductReservation.objects.get_or_create(
            product_size=product_size_obj,
            session_key=session_key,
            defaults={"quantity": quantity},
        )
        if not created:
            # If the reservation already exists, increase the quantity
            reservation.quantity += quantity
            reservation.save()


def set_or_update_checkout_expiry(request):
    '''
    Set or update the cart expiration time in the session and schedule
    a task to release the reserved products after the specified time
    '''
    existing_task_id = request.session.get("current_checkout_task_id")
    if existing_task_id:
        celery_app.control.revoke(existing_task_id, terminate=True)
        del request.session["clear_cart_task_id"]

    # Schedule the new task and store its ID in the session
    countdown = int(settings.CHECKOUT_EXPIRY_MINUTES) * 60

    product_size_ids = list(request.session.get("bag", {}).keys())
    session_key = request.session.session_key
    task = release_reserving_products.apply_async(
        (product_size_ids, session_key), countdown=countdown
    )

    # Update the time of the product reservations that are in the bag
    reservations = ProductReservation.objects.filter(
        product_size__in=product_size_ids
    )
    reservations.update(reversed_at=timezone.now())

    request.session["clear_cart_task_id"] = task.id
    # add the task expiry time to the session
    request.session["cart_expiration_time"] = (
        timezone.now() + timezone.timedelta(seconds=countdown)
    ).isoformat()
    request.session.modified = True
