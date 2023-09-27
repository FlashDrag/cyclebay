from django.db.models import Case, When, BooleanField
from django.db.models.query import QuerySet
from django.contrib.auth import get_user_model

User = get_user_model()


def annotate_saved_products(products: QuerySet, user: User):
    """
    Annotate a list of products with is_in_wishlist attribute.
    Set is_in_wishlist to True if the product is in the user's wishlist.
    """
    # get the ids of the favorite product
    favorite_product_ids = user.wishlist.products.values_list("id", flat=True)

    # set is_in_wishlist to True if the product id is in favorite_product_ids
    annotated_products = products.annotate(
        is_in_wishlist=Case(
            When(id__in=favorite_product_ids, then=True),
            default=False,
            output_field=BooleanField(),
        )
    )
    return annotated_products
