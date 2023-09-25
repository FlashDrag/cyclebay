from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages


from products.models import Product, ProductSize, Size


def view_bag(request):
    """A view to return the bag contents page"""

    return render(request, "bag/bag.html")


def add_to_bag(request, item_id):
    """Add a product to the shopping bag"""

    # TODO: refactor get_object_or_404 to a try/except block
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

    # TODO: refactor get_object_or_404 to a try/except block check if product_size_obj is exists  # noqa
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

    bag = request.session.get("bag", {})

    if product_size_id in list(bag.keys()):
        # If the product size is already in the bag, check if the
        # quantity is greater than the number of available products
        if product_size_obj.count < bag[product_size_id] + 1:
            messages.error(
                request,
                f"Sorry, only <b>{product_size_obj.count}</b> "
                f"<b>{product_size_obj}</b> available.\n"
                f"Please check your cart!",
                extra_tags="safe",
            )
        # If the quantity is less than the number of available products,
        # increment the quantity by 1
        else:
            bag[product_size_id] += 1
            messages.success(
                request,
                f"Updated <b>{product_size_obj}</b> quantity "
                f"to <b>{bag[product_size_id]}</b>",
                extra_tags="safe",
            )
    else:
        # If the product size is not in the bag, add it to the bag
        bag[product_size_id] = 1
        messages.success(
            request,
            f"Added <b>{product_size_obj}</b> to your cart",
            extra_tags="safe",
        )

    request.session["bag"] = bag

    return redirect(redirect_url)


def adjust_bag(request, product_size_id):
    """
    Adjust the quantity of the specified product_size to the specified amount
    """

    # TODO: refactor get_object_or_404 to a try/except block
    product_size_obj = get_object_or_404(ProductSize, pk=product_size_id)
    bag = request.session.get("bag", {})

    quantity = int(request.POST.get("quantity"))

    if quantity > 0:
        if quantity > product_size_obj.count:
            # If the product is out of stock pass
            if product_size_obj.count == 0:
                pass
            # If the quantity is greater than the number of available products,
            # return a warning message
            else:
                product_plural = (
                    "product is"
                    if product_size_obj.count == 1
                    else "products are"  # noqa
                )
                messages.warning(
                    request,
                    f"Only <b>{product_size_obj.count}</b> {product_plural} available",  # noqa
                    extra_tags="safe",
                )
        else:
            bag[product_size_id] = quantity
            messages.success(
                request,
                f"Updated <b>{product_size_obj}</b> quantity"
                f" to <b>{bag[product_size_id]}</b>",
                extra_tags="safe",
            )

    else:
        # TODO: refactor get_object_or_404 to a try/except block check if product_size_obj is exists  # noqa
        # Remove the product size item from the bag
        bag.pop(product_size_id)
        messages.success(
            request,
            f"Removed <b>{product_size_obj}</b> from your cart",  # noqa
            extra_tags="safe",
        )

    request.session["bag"] = bag

    return redirect(reverse("view_bag"))


def remove_from_bag(request, product_size_id):
    """Remove the product size item from the shopping bag and
    release the reserved products"""

    # Remove the product size item from the bag
    bag = request.session.get("bag", {})
    bag.pop(product_size_id)
    request.session["bag"] = bag

    try:
        product_size_obj = ProductSize.objects.get(pk=product_size_id)
        msg = f"Removed <b>{product_size_obj}</b> from your cart"
    except ProductSize.DoesNotExist:
        msg = "Removed from your cart"

    messages.success(request, msg, extra_tags="safe")

    return HttpResponse(status=200)
