from django import forms
from products.models import Product, Category, Brand, Size, Color

from .widgets import CustomClearableFileInput
from products.models import ProductSize


# TODO: User must be able to add quantity for each size


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ("image_url",)

        help_texts = {
            "featured": "Tick this box if you want to offer this product "
            "as a special offer.",
        }

    field_order = [
        'category',
        'brand',
        'sku',
        'name',
        'price',
        'color',
        'sizes',
        'count',
        'featured',
        'image',
    ]

    image = forms.ImageField(
        label="Image", required=False, widget=CustomClearableFileInput
    )
    count = forms.IntegerField(min_value=1, initial=1)
    sizes = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set required fields
        self.fields["sku"].required = True
        self.fields["category"].required = True
        self.fields["color"].required = True
        self.fields["brand"].required = True

        # Change field labels
        self.fields["sku"].label = "SKU"
        self.fields["count"].label = "Quantity"
        self.fields["sizes"].label = "Size"
        self.fields["featured"].label = "Special Offer"

        # Add placeholders
        self.fields["sku"].widget.attrs["placeholder"] = "e.g. XYZ12345"
        self.fields["name"].widget.attrs[
            "placeholder"
        ] = "e.g. Cube Access Hybrid Pro 500"
        self.fields["price"].widget.attrs["placeholder"] = "e.g. 899.99"

        # Set friendly names for categories, brands,
        # sizes and colors
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

        sizes = Size.objects.all()
        size_friendly_names = [
            (size.id, size.get_friendly_name()) for size in sizes
        ]
        self.fields["sizes"].choices = size_friendly_names

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
