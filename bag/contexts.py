from decimal import Decimal
from django.conf import settings
from django.contrib import messages

from products.models import ProductSize


def bag_contents(request):
    """Allows bag contents to be available across the entire website"""
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get("bag", {})
    bag_copy = bag.copy()

    for product_size_id, product_size_count in bag_copy.items():

        try:
            product_size_obj = ProductSize.objects.get(pk=product_size_id)

            # If the product size count in the bag is greater than the
            # product size count in the database:
            if product_size_obj.count < product_size_count:
                product_size_count = product_size_obj.count

                if product_size_obj.count == 0:
                    messages.error(
                        request,
                        f"Sorry, <b>{product_size_obj}</b> no longer available",  # noqa
                        extra_tags="safe",
                        )
                else:
                    messages.warning(
                        request,
                        f"Only <b>{product_size_count}</b> <b>{product_size_obj}</b> available",  # noqa
                        extra_tags="safe",
                    )
                # update the bag with the product size count in db
                bag[product_size_id] = product_size_count

            # Add the product size to the bag
            product = product_size_obj.product
            total += product_size_count * product.price
            product_count += product_size_count
            bag_items.append(
                {
                    "product_size_id": product_size_id,
                    "product_size_obj": product_size_obj,
                    "quantity": product_size_count,
                    "product": product,
                    "size": product_size_obj.size,
                    "color": product.color,
                }
            )
        except ProductSize.DoesNotExist:
            # If the product size object does not exist in the database,
            # remove it from the bag
            bag.pop(product_size_id)
            request.session["bag"] = bag
            messages.error(
                request,
                "Sorry, one of the products in your bag is no longer available",  # noqa
            )
        finally:
            request.session.modified = True

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
    }

    return context
