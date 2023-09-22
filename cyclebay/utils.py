from cyclebay.celery import app as celery_app
from django.utils import timezone
from django.conf import settings
from bag.tasks import release_reserving_products


def clear_cart_task(request):
    '''
    Clear the cart and release the reserved products
    after the cart expiry time has passed using Celery
    '''
    # Revoking the previous task, as a new checkout has been initiated
    existing_task_id = request.session.get("clear_cart_task_id")
    if existing_task_id:
        celery_app.control.revoke(existing_task_id)
        del request.session["clear_cart_task_id"]

    # Schedule the new task and store its ID in the session
    countdown = int(settings.CART_EXPIRY_MINUTES) * 60
    task = release_reserving_products.apply_async(
        (request.session.session_key,), countdown=countdown
    )
    request.session["clear_cart_task_id"] = task.id
    # add the task expiry time to the session
    request.session["cart_expiration_time"] = (
        timezone.now() + timezone.timedelta(seconds=countdown)
    ).isoformat()
    request.session.modified = True
