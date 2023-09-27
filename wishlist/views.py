from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from products.models import Product
from .models import Wishlist


@login_required
def wishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    context = {
        'wishlist': wishlist.products.all(),
    }
    return render(request, 'wishlist/wishlist.html', context)


@login_required
@require_POST
def add_to_wishlist_toggle(request, product_id):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, pk=product_id)

    if product in wishlist.products.all():
        wishlist.products.remove(product)
        wishlist.save()
        is_in_wishlist = False
        msg = f"<b>{product.name}</b> removed from your wishlist"
    else:
        wishlist.products.add(product)
        wishlist.save()
        is_in_wishlist = True
        msg = f"<b>{product.name}</b> added to your wishlist"

    return JsonResponse(
        {
            'is_in_wishlist': is_in_wishlist,
            'wishlist_message': msg,
        }
    )
