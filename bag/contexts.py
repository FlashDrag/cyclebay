from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import ProductSize


def bag_contents(request):
    """Allows bag contents to be available across the entire website"""
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get("bag", {})

    for product_size_id, product_size_count in bag.items():
        product_size_obj = get_object_or_404(
            ProductSize, pk=product_size_id
        )
        product = product_size_obj.product
        total += product_size_count * product.price
        product_count += product_size_count
        bag_items.append(
            {
                "product_size_id": product_size_id,
                "quantity": product_size_count,
                "product": product,
                "size": product_size_obj.size,
            }
        )

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    is_expired_msg_shown = request.session.get("is_expired_msg_shown", False)

    context = {
        "bag_items": bag_items,
        "total": total,
        "product_count": product_count,
        "delivery": delivery,
        "free_delivery_delta": free_delivery_delta,
        "free_delivery_threshold": settings.FREE_DELIVERY_THRESHOLD,
        "grand_total": grand_total,
        "cart_expiration_time": request.session.get("cart_expiration_time"),
        "is_expired_msg_shown": is_expired_msg_shown,
    }

    return context
