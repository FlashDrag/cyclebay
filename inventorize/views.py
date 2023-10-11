from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.urls import reverse

from products.models import Product, ProductSize, Size
from .forms import ProductForm, create_product_size_formset


@login_required
def add_product(request):
    """Add a product to the store"""

    ProductSizeFormSet = create_product_size_formset()

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

            messages.info(
                request,
                f"<b>{product.name}</b> successfully added",
                extra_tags="safe",
            )
            return redirect(reverse("product_detail", args=[product.id]))
        else:
            for sub_form, size in zip(formset.forms, Size.objects.all()):
                sub_form.size_friendly_name = size.friendly_name
                sub_form.size_name = size.name
            messages.error(
                request,
                "Failed to add product. Please ensure the form is valid.",
            )
    else:
        form = ProductForm()
        sizes = Size.objects.all()
        formset = ProductSizeFormSet(
            queryset=ProductSize.objects.none(),
            prefix="sizes",
            # set the initial value for each form in the formset
            initial=[{"size": size} for size in sizes],
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


@login_required
def edit_product(request, product_id):
    """Edit a product in the store"""

    ProductSizeFormSet = create_product_size_formset()

    # only store owners can manage products
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only store owners can do that.")
        return redirect(reverse("home"))

    product = get_object_or_404(Product, pk=product_id)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = ProductSizeFormSet(request.POST, prefix="sizes")
        if form.is_valid() and formset.is_valid():
            form.save()

            # Manage product sizes
            for sub_form in formset.forms:
                # product size instance
                instance = sub_form.instance
                # product size cleaned data that includes:
                # Size instance, count, and DELETE
                cleaned_data = sub_form.cleaned_data
                try:
                    # Check if a ProductSize instance exists for the
                    # current size and product
                    product_size = ProductSize.objects.get(
                        product=product, size=cleaned_data.get("size")
                    )
                    # If it exists, but the DELETE checkbox is checked,
                    # delete the ProductSize record
                    if cleaned_data.get("DELETE"):
                        product_size.delete()
                    else:
                        # Otherwise, update the count
                        product_size.count = sub_form.cleaned_data.get(
                            "count", 0
                        )
                        product_size.save()
                except ProductSize.DoesNotExist:
                    # If it doesn't exist and the DELETE checkbox is not
                    # checked, create a new ProductSize instance
                    if not cleaned_data.get("DELETE"):
                        instance.product = product
                        instance.save()

            messages.info(
                request,
                f"<b>{product.name}</b> successfully updated!",
                extra_tags="safe",
            )
            return redirect(reverse("product_detail", args=[product.id]))
        else:
            for sub_form, size in zip(formset.forms, Size.objects.all()):
                sub_form.size_friendly_name = size.friendly_name
                sub_form.size_name = size.name
            messages.error(
                request,
                "Failed to update product. Please ensure the form is valid.",
            )
    else:
        form = ProductForm(instance=product)
        sizes = Size.objects.all()
        initial_data = []
        for size in sizes:
            # Check if a ProductSize instance exists for
            # the current size and product
            product_size = ProductSize.objects.filter(
                product=product, size=size
            ).first()
            if product_size:
                # If it exists, use the existing count and
                # set DELETE to False
                initial_data.append(
                    {
                        "size": size,
                        "count": product_size.count,
                        "DELETE": False,
                    }
                )
            else:
                # If it doesn't exist, use default count 0 and
                # set DELETE to True
                initial_data.append({"size": size, "count": 0, "DELETE": True})
        formset = ProductSizeFormSet(
            queryset=ProductSize.objects.filter(product=product),
            initial=initial_data,
            prefix="sizes",
        )

        for sub_form, size in zip(formset.forms, sizes):
            sub_form.size_friendly_name = size.friendly_name
            sub_form.size_name = size.name

        messages.info(
            request,
            f"You are editing <b>{product.name}</b>",
            extra_tags="safe",
        )

    template = "inventorize/edit_product.html"
    context = {
        "form": form,
        "formset": formset,
        "product": product,
    }

    return render(request, template, context)


@login_required
@require_POST
def delete_product(request, product_id):
    """Delete a product from the store"""

    # only store owners can manage products
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only store owners can do that.")
        return HttpResponse(status=403)

    try:
        product = Product.objects.get(pk=product_id)
        product_name = product.name
        product.delete()
        messages.info(
            request, f"<b>{product_name}</b> deleted!", extra_tags="safe"
        )
    except Product.DoesNotExist:
        messages.error(request, "Sorry, this product does not exist")
        return HttpResponse(status=404)
    else:
        return HttpResponse(status=200)
