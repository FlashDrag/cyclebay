import stripe
from django.db import transaction
from django.db.models import F
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.models import Site


from .models import Order, OrderLineItem
from profiles.models import UserProfile
from products.models import ProductSize

import json
import time

from datetime import datetime


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        current_site = Site.objects.get_current()
        cust_email = order.email
        subject = render_to_string(
            "checkout/confirmation_emails/confirmation_email_subject.txt",
            {"order": order, "current_site": current_site},
        )
        body = render_to_string(
            "checkout/confirmation_emails/confirmation_email_body.txt",
            {
                "order": order,
                "contact_email": settings.DEFAULT_FROM_EMAIL,
                "current_site": current_site,
            },
        )

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email],
        )

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}', status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = True if intent.metadata.save_info == "true" else False

        charge = stripe.Charge.retrieve(intent.latest_charge)
        billing_details = charge.billing_details
        shipping_details = intent.shipping
        receipt_url = charge.receipt_url
        metadata = charge.metadata
        grand_total = round(charge.amount / 100, 2)

        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # Update profile information if save_info was checked
        profile = None
        user = intent.metadata.user
        if user != "AnonymousUser":
            profile = UserProfile.objects.get(user__email=user)
            if save_info:
                # Save the user's name to the User model
                User = get_user_model()
                current_user = User.objects.get(email=user)
                current_user.name = shipping_details.name
                current_user.save()

                # Save the user's info to the UserProfile model
                profile.default_phone_number = shipping_details.phone
                profile.default_country = shipping_details.address.country
                profile.default_postcode = shipping_details.address.postal_code
                profile.default_town_or_city = shipping_details.address.city
                profile.default_street_address1 = (
                    shipping_details.address.line1
                )
                profile.default_street_address2 = (
                    shipping_details.address.line2
                )
                profile.default_county = shipping_details.address.state
                profile.save()

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)
        if order_exists:
            self._send_confirmation_email(order)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} |'
                " SUCCESS: Verified order already in database",
                status=200,
            )
        else:
            order = None
            with transaction.atomic():
                # savepoint allows to rollback the transaction;
                # in this case, it is used to manually rollback the
                # transaction as the raised exception is handled
                savepoint = transaction.savepoint()
                try:
                    order = Order.objects.create(
                        full_name=shipping_details.name,
                        user_profile=profile,
                        email=billing_details.email,
                        phone_number=shipping_details.phone,
                        country=shipping_details.address.country,
                        postcode=shipping_details.address.postal_code,
                        town_or_city=shipping_details.address.city,
                        street_address1=shipping_details.address.line1,
                        street_address2=shipping_details.address.line2,
                        county=shipping_details.address.state,
                        delivery_cost=metadata.get("delivery_cost", 0),
                        order_total=metadata.get("order_total", 0),
                        grand_total=metadata.get("grand_total", 0),
                        original_bag=bag,
                        stripe_pid=pid,
                        receipt_url=receipt_url,
                    )
                    for item in json.loads(bag):
                        product_size_id = item.get("product_size_id")
                        item_quantity = item.get("quantity")
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
                            quantity=item_quantity,
                        )
                        order_line_item.save()

                        # update the product size count in stock
                        product_size_obj.count = F("count") - item_quantity
                        product_size_obj.save()
                except Exception as e:
                    # rollback the transaction if there is an error
                    transaction.savepoint_rollback(savepoint)
                    if order:
                        order.delete()
                    return HttpResponse(
                        content=f'Webhook received: {event["type"]} | ERROR: {e}',  # noqa
                        status=500,
                    )
        self._send_confirmation_email(order)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} |'
            " SUCCESS: Created order in webhook",
            status=200,
        )

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        print("handle_payment_intent_payment_failed", datetime.now())
        return HttpResponse(
            content=f'Webhook received: {event["type"]}', status=200
        )
