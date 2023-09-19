from celery import shared_task
from django.db import transaction

from .models import ProductReservation


@shared_task
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

        # TODO: clear the bag by setting the session bag to an empty dict


