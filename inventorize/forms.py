from django import forms
from django.forms import inlineformset_factory

from products.models import (
    Product,
    Category,
    Brand,
    Size,
    Color,
    validate_color,
)

from .widgets import CustomClearableFileInput
from products.models import ProductSize


class ProductForm(forms.ModelForm):
    new_category_name = forms.CharField(
        max_length=254,
        required=False,
        label="Category Name*",
    )
    new_category_friendly_name = forms.CharField(
        max_length=254,
        required=False,
        label="Category Friendly Name",
    )

    new_brand_name = forms.CharField(
        max_length=254,
        required=False,
        label="Brand Name*",
    )
    new_brand_friendly_name = forms.CharField(
        max_length=254,
        required=False,
        label="Brand Friendly Name",
    )

    new_color_name = forms.CharField(
        max_length=7,
        required=False,
        label="",
        validators=[validate_color],
    )
    new_color_friendly_name = forms.CharField(
        max_length=254,
        required=False,
        label="Enter Color Friendly Name",
    )

    class Meta:
        model = Product
        exclude = ("image_url", "sizes")

        help_texts = {
            "featured": "Tick this box if you want to offer this product "
            "as a special offer.",
        }

    field_order = [
        "category",
        "new_category_name",
        "new_category_friendly_name",
        "brand",
        "new_brand_name",
        "new_brand_friendly_name",
        "sku",
        "name",
        "price",
        "color",
        "new_color_name",
        "new_color_friendly_name",
        "featured",
        "image",
    ]

    image = forms.ImageField(
        label="Image", required=False, widget=CustomClearableFileInput
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set required fields
        self.fields["sku"].required = True
        self.fields["category"].required = True
        self.fields["color"].required = True
        self.fields["brand"].required = True

        # Change field labels
        self.fields["sku"].label = "SKU"
        self.fields["featured"].label = "Special Offer"

        # Add placeholders
        self.fields["new_category_name"].widget.attrs[
            "placeholder"
        ] = "e.g. kids-bikes"
        self.fields["new_category_friendly_name"].widget.attrs[
            "placeholder"
        ] = "e.g. Kids Bikes"
        self.fields["new_brand_name"].widget.attrs["placeholder"] = "e.g. cube"
        self.fields["new_brand_friendly_name"].widget.attrs[
            "placeholder"
        ] = "e.g. Cube"
        self.fields["new_color_name"].widget.attrs[
            "placeholder"
        ] = "e.g. #800080"
        self.fields["new_color_friendly_name"].widget.attrs[
            "placeholder"
        ] = "e.g. Purple"
        self.fields["sku"].widget.attrs["placeholder"] = "e.g. XYZ12345"
        self.fields["name"].widget.attrs[
            "placeholder"
        ] = "e.g. Cube Access Hybrid Pro 500"
        self.fields["price"].widget.attrs["placeholder"] = "e.g. 899.99"

        # Set friendly names for categories, brands, and colors
        categories = Category.objects.all()
        category_friendly_names = [
            (category.id, category.get_friendly_name())
            for category in categories
        ]
        self.fields["category"].choices = category_friendly_names

        brands = Brand.objects.all()
        brand_friendly_names = [
            (brand.id, brand.get_friendly_name()) for brand in brands
        ]
        self.fields["brand"].choices = brand_friendly_names

        colors = Color.objects.all()
        color_friendly_names = [
            (color.id, color.get_friendly_name()) for color in colors
        ]
        self.fields["color"].choices = color_friendly_names

        # Add classes to form fields
        for field_name, field in self.fields.items():
            if field_name not in ["image", "featured"]:
                field.widget.attrs[
                    "class"
                ] = "border-black rounded-0 management-style-input"

    def save(self, commit=True):
        product = super().save(commit=False)

        # Get the new category name and friendly name from the form,
        # if they exist, and create a new category and assign it to the product
        new_category_name = self.cleaned_data["new_category_name"]
        new_category_friendly_name = self.cleaned_data[
            "new_category_friendly_name"
        ]
        if new_category_name.strip():
            if new_category_friendly_name.strip():
                category, created = Category.objects.get_or_create(
                    name=new_category_name,
                    friendly_name=new_category_friendly_name,
                )
            else:
                category, created = Category.objects.get_or_create(
                    name=new_category_name,
                    friendly_name=new_category_name,
                )

            product.category = category

        # Get the new brand name and friendly name from the form,
        # if they exist, and create a new brand and assign it to the product
        new_brand_name = self.cleaned_data["new_brand_name"]
        new_brand_friendly_name = self.cleaned_data["new_brand_friendly_name"]
        if new_brand_name.strip():
            if new_brand_friendly_name.strip():
                brand, created = Brand.objects.get_or_create(
                    name=new_brand_name,
                    friendly_name=new_brand_friendly_name,
                )
            else:
                brand, created = Brand.objects.get_or_create(
                    name=new_brand_name,
                    friendly_name=new_brand_name,
                )

            product.brand = brand

        # Get the new color name and friendly name from the form,
        # if they exist, and create a new color and assign it to the product
        new_color_name = self.cleaned_data["new_color_name"]
        new_color_friendly_name = self.cleaned_data["new_color_friendly_name"]
        if new_color_name.strip():
            if new_color_friendly_name.strip():
                color, created = Color.objects.get_or_create(
                    name=new_color_name,
                    friendly_name=new_color_friendly_name,
                )
            else:
                color, created = Color.objects.get_or_create(
                    name=new_color_name,
                    friendly_name=new_color_name,
                )

            product.color = color

        if commit:
            product.save()
        return product


class ProductSizeForm(forms.ModelForm):
    class Meta:
        model = ProductSize
        fields = ("size", "count")
        # hide the size select input to prevent the user from
        # selecting the same size more than once
        widgets = {"size": forms.HiddenInput()}
        labels = {
            "count": "Quantity",
        }


def create_product_size_formset():
    '''
    Create a formset for the ProductSize model.

    The formset allows to create multiple forms for each size
    of a product, and to edit the quantity of each size.
    '''
    return inlineformset_factory(
        Product,
        ProductSize,
        form=ProductSizeForm,
        extra=Size.objects.count(),
        can_delete=True,
    )
