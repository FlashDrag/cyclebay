from celery import shared_task
from django.db import transaction
from django.contrib.sessions.backends.db import SessionStore

from .models import ProductReservation


@shared_task(ignore_result=True)
def release_reserving_products(session_key):
    """
    Release reserving products, return them to stock and
    clear the bag
    """
    reservations = ProductReservation.objects.filter(
        session_key=session_key
    )
    with transaction.atomic():
        for reservation in reservations:
            reservation.product_size.count += reservation.quantity
            reservation.product_size.save()

        ProductReservation.objects.filter(
            session_key=session_key
        ).delete()

        # Clear the session bag
        store = SessionStore(session_key=session_key)
        store["bag"] = {}
        # Since the task is executed, remove the task ID from the session
        store["clear_cart_task_id"] = None
        store.save()
