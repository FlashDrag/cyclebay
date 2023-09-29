from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from products.models import Product, ProductSize, Size
from .forms import ProductForm, ProductSizeFormSet


@login_required
def add_product(request):
    """Add a product to the store"""

    # only store owners can manage products
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only store owners can do that.")
        return redirect(reverse("home"))

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        formset = ProductSizeFormSet(request.POST, prefix="sizes")

        if form.is_valid() and formset.is_valid():
            product = form.save()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.product = product
                instance.save()

            messages.success(request, "Successfully added product!")
            return redirect(reverse("product_detail", args=[product.id]))
        else:
            messages.error(
                request,
                "Failed to add product. Please ensure the form is valid.",
            )
    else:
        form = ProductForm()
        sizes = Size.objects.all()
        formset = ProductSizeFormSet(
            queryset=ProductSize.objects.none(), prefix="sizes",
            # set the initial value for each form in the formset
            initial=[{"size": size} for size in sizes]
        )
        # add additional attributes to each form in the formset,
        # that include the size name and size friendly name
        for sub_form, size in zip(formset.forms, sizes):
            sub_form.size_friendly_name = size.friendly_name
            sub_form.size_name = size.name

    template = "inventorize/add_product.html"
    context = {
        "form": form,
        "formset": formset,
    }

    return render(request, template, context)
