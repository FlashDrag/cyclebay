from celery import shared_task
from django.db import transaction
from django.contrib.sessions.backends.db import SessionStore

from .models import ProductReservation


@shared_task
def release_reserving_products(product_size_ids, session_key):
    """
    Release reserving products, return them to stock,
    clear the bag, cart expiration time and task ID
    """
    reservations = ProductReservation.objects.filter(
        # TODO exat match
        product_size__in=product_size_ids,
    )
    with transaction.atomic():
        for reservation in reservations:
            reservation.product_size.count += reservation.quantity
            reservation.product_size.save()

        ProductReservation.objects.filter(
            # TODO exat match
            product_size__in=product_size_ids,
        ).delete()

    try:
        store = SessionStore(session_key=session_key)
        # Clear the session bag
        store["bag"] = {}
        # Since the task is executed, remove the task ID from the session
        store["clear_cart_task_id"] = None
        # Remove the cart expiration time from the session
        store.session["cart_expiration_time"] = None
        store.save()
    except Exception:
        pass
