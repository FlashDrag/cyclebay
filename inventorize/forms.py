from django import forms
from django.forms import inlineformset_factory

from products.models import Product, Category, Brand, Size, Color

from .widgets import CustomClearableFileInput
from products.models import ProductSize


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ("image_url", "sizes")

        help_texts = {
            "featured": "Tick this box if you want to offer this product "
            "as a special offer.",
        }

    field_order = [
        "category",
        "brand",
        "sku",
        "name",
        "price",
        "color",
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


class ProductSizeForm(forms.ModelForm):
    class Meta:
        model = ProductSize
        fields = ("size", "count")
        # hide the size select input to prevent the user from
        # selecting the same size more than once
        widgets = {'size': forms.HiddenInput()}
        labels = {
            "count": "Quantity",
        }


# The formset allows to create multiple forms for each size
# of a product, and to edit the quantity of each size.
ProductSizeFormSet = inlineformset_factory(
    Product,
    ProductSize,
    form=ProductSizeForm,
    extra=Size.objects.count(),
    can_delete=True,
)
