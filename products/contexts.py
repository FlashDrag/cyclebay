from products.models import Category


def all_categories(request):
    """Allows categories to be available across the entire website,
    so that they can be used in the navbar and footer"""
    categories = Category.objects.all()

    context = {
        "all_categories": categories,
    }

    return context
