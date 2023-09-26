from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from checkout.models import Order
from .models import UserProfile


class OrderAdminInline(admin.TabularInline):
    """Allows admin to view order details from the user profile page"""
    model = Order
    extra = 0
    show_change_link = True
    readonly_fields = (
        'order_number_link',
        "date",
        "grand_total",
        "original_bag",
    )

    fields = (
        'order_number_link',
        "date",
        "grand_total",
        "original_bag",
    )

    def order_number_link(self, obj):
        """Create a link to the order detail page.
        Allows admin to click on the order number"""
        url = reverse("admin:checkout_order_change", args=[obj.pk])
        return format_html('<a href="{}">{}</a>', url, obj.order_number)

    order_number_link.short_description = "Order Number"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    inlines = (OrderAdminInline,)

    list_display = (
        "user",
        "default_phone_number",
    )
