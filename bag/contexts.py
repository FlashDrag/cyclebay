from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404

from .models import ProductReservation
from products.models import ProductSize


def bag_contents(request):
    """Allows bag contents to be available across the entire website"""
    bag_items = []
    total = 0
    product_count = 0
    # request.session["bag"] = {}

    product_size_ids = list(map(int, request.session.get("bag", {}).keys()))
    print('product_size_ids:', product_size_ids)
    reservations = ProductReservation.objects.filter(
        # TODO exat match
        product_size__in=product_size_ids
    )
    print('reservations:', reservations)

    for reservation in reservations:
        product_size_obj = reservation.product_size
        product = product_size_obj.product
        total += reservation.quantity * product.price
        product_count += reservation.quantity
        bag_items.append(
            {
                "product_size_id": product_size_obj.id,
                "product_size_obj": product_size_obj,
                "quantity": reservation.quantity,
                "product": product,
                "size": product_size_obj.size,
                "color": product.color,
            }
        )

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        "bag_items": bag_items,
        "total": total,
        "product_count": product_count,
        "delivery": delivery,
        "free_delivery_delta": free_delivery_delta,
        "free_delivery_threshold": settings.FREE_DELIVERY_THRESHOLD,
        "grand_total": grand_total,
        "cart_expiration_time": request.session.get("cart_expiration_time"),
    }

    return context
