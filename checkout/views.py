import stripe
import json

from django.db.models import F
from django.db import transaction
from django.shortcuts import (
    render,
    redirect,
    reverse,
    get_object_or_404,
    HttpResponse,
)
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import get_user_model

from profiles.forms import UserProfileForm
from profiles.models import UserProfile
from products.models import Product, ProductSize
from bag.contexts import bag_contents

from .forms import OrderForm
from .models import Order, OrderLineItem


@require_POST
def cache_checkout_data(request):

    # Verify that the bag hasn't changed between the time
    # the user started the checkout and when they submitted the form
    session_bag = request.session.get("bag", {})
    # make a copy of the bag in the session to compare with the updated bag
    session_bag_copy = session_bag.copy()
    # call the bag_contents function from contexts.py to update the bag
    current_bag = bag_contents(request)
    updated_bag = {
        item["product_size_id"]: item["quantity"]
        for item in current_bag["bag_items"]  # noqa
    }
    # Bag consistency check
    if session_bag_copy != updated_bag:
        messages.error(
            request,
            "The payment not processed because there was a change in your bag."
        )
        return HttpResponse(status=400, content="Bag changed")

    # Clean the bag with empty product sizes
    bag_for_metadata = []
    for item in current_bag["bag_items"]:
        if item["quantity"] > 0:
            bag_for_metadata.append(
                {
                    "product_id": item["product"].id,
                    "product_name": item["product"].name,
                    "product_size_id": item["product_size_id"],
                    "size": item["size"].name,
                    "quantity": item["quantity"],
                    "price": str(item["product"].price),
                    "color": item["product"].color.name,
                }
            )

    pid = request.POST.get("client_secret").split("_secret")[0]
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        stripe.PaymentIntent.modify(
            pid,
            metadata={
                "bag": json.dumps(bag_for_metadata),
                "save_info": request.POST.get("save_info"),
                "user": request.user,
                "order_total": current_bag["total"],
                "delivery_cost": current_bag["delivery"],
                "grand_total": current_bag["grand_total"],
            },
        )
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(
            request,
            "Sorry, your payment cannot be \
            processed right now. Please try again later.",
        )
        return HttpResponse(content=e, status=400)


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    stripe.api_key = stripe_secret_key

    if request.method == "POST":
        # clean the bag with empty product sizes
        bag = {
            product_size_id: quantity
            for product_size_id, quantity in request.session["bag"].items()
            if quantity > 0
        }

        form_data = {
            "full_name": request.POST["full_name"],
            "email": request.POST["email"],
            "phone_number": request.POST["phone_number"],
            "country": request.POST["country"],
            "postcode": request.POST["postcode"],
            "town_or_city": request.POST["town_or_city"],
            "street_address1": request.POST["street_address1"],
            "street_address2": request.POST["street_address2"],
            "county": request.POST["county"],
        }
        order_form = OrderForm(form_data)
        # transaction.atomic() ensures all database operations are
        # completed successfully
        if order_form.is_valid():
            order = order_form.save(commit=False)
            # get receipt_url from the stripe Charge object
            intent = stripe.PaymentIntent.retrieve(
                request.POST.get("client_secret").split("_secret")[0]
            )
            charge = stripe.Charge.retrieve(intent.latest_charge)
            metadata = charge.metadata
            receipt_url = charge.receipt_url

            pid = request.POST.get("client_secret").split("_secret")[0]
            order.stripe_pid = pid
            order.order_total = metadata.get("order_total", 0)
            order.delivery_cost = metadata.get("delivery_cost", 0)
            order.grand_total = metadata.get("grand_total", 0)
            order.receipt_url = receipt_url
            order.original_bag = metadata.get("bag", "")
            order.save()
            with transaction.atomic():
                # savepoint allows to rollback the transaction;
                # in this case, it is used to manually rollback the
                # transaction as the raised exception is handled
                savepoint = transaction.savepoint()
                for product_size_id, quantity in bag.items():
                    try:
                        # select_for_update allows to lock the selected
                        # product size to prevent race conditions until
                        # the transaction is complete
                        product_size_obj = ProductSize.objects.select_for_update().get(  # noqa
                            pk=product_size_id
                        )
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product_size_obj.product,
                            product_size=product_size_obj,
                            quantity=quantity,
                        )
                        order_line_item.save()

                        # Decrease the product size quantity
                        product_size_obj.count = F("count") - quantity
                        product_size_obj.save()
                    except Product.DoesNotExist:
                        # rollback the transaction if there is an error
                        transaction.savepoint_rollback(savepoint)
                        order.delete()
                        messages.error(
                            request,
                            (
                                "One of the products in your bag wasn't"
                                " found in our database.\n"
                                "Please call us for assistance!"
                            ),
                        )
                        return redirect(reverse("view_bag"))

            request.session["save_info"] = bool(request.POST.get("save_info"))
            return redirect(
                reverse("checkout_success", args=[order.order_number])
            )
        else:
            messages.error(
                request,
                "There was an error with your form. \
                Please double check your information.",
            )
    else:
        # call the bag_contents function from contexts.py to update the bag
        # in the session
        current_bag = bag_contents(request)
        if not current_bag.get("bag_items") or current_bag["total"] == 0:
            messages.warning(
                request,
                "There's nothing in your cart at the moment.\n"
                "Return to shopping.",
            )
            return redirect(reverse("products"))

        total = current_bag["grand_total"]
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(
                    initial={
                        "full_name": profile.user.name,
                        "email": profile.user.email,
                        "phone_number": profile.default_phone_number,
                        "country": profile.default_country,
                        "postcode": profile.default_postcode,
                        "town_or_city": profile.default_town_or_city,
                        "street_address1": profile.default_street_address1,
                        "street_address2": profile.default_street_address2,
                        "county": profile.default_county,
                    }
                )
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(
            request,
            "Stripe public key is missing. \
            Did you forget to set it in your environment?",
        )

    template = "checkout/checkout.html"
    context = {
        "order_form": order_form,
        "stripe_public_key": stripe_public_key,
        "client_secret": intent.client_secret,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get("save_info")
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        # Attach the user's profile to the order
        profile = UserProfile.objects.get(user=request.user)
        order.user_profile = profile
        order.save()

        # Save the user's info
        if save_info:
            profile_data = {
                "name": order.full_name,
                "default_phone_number": order.phone_number,
                "default_country": order.country,
                "default_postcode": order.postcode,
                "default_town_or_city": order.town_or_city,
                "default_street_address1": order.street_address1,
                "default_street_address2": order.street_address2,
                "default_county": order.county,
            }
            user_profile_form = UserProfileForm(
                profile_data,
                instance=profile,
                user=request.user
                )
            if user_profile_form.is_valid():
                user_profile_form.save()
    else:
        # Save the order to the user's profile if the user is not authenticated
        # but has a profile for the email used in the order
        try:
            User = get_user_model()
            user = User.objects.get(email=order.email)
            profile = UserProfile.objects.get(user=user)
            order.user_profile = profile
            order.save()
            messages.info(
                request,
                "Your order has been saved to an existing profile "
                f"with the email <b>{profile.user.email}</b>.",
                extra_tags="safe",
            )
        except (User.DoesNotExist, UserProfile.DoesNotExist):
            pass

    messages.success(
        request,
        f"Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.",
    )

    if "bag" in request.session:
        del request.session["bag"]

    template = "checkout/checkout_success.html"
    context = {
        "order": order,
        "order_items": json.loads(order.original_bag),
    }

    return render(request, template, context)
