from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    name = forms.CharField(
        max_length=254,
        widget=forms.TextInput(
            attrs={
                "class": "border-black rounded-0 profile-form-input",
                "placeholder": "Name *",
            }
        ),
    )

    class Meta:
        model = UserProfile
        exclude = ("user",)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        # pop the user argument if it exists
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        # If 'user' is provided and it has a 'name', set the initial value
        if user and hasattr(user, 'name'):
            self.fields['name'].initial = user.name

        # Set order of fields
        self.order_fields(
            [
                "name",
                "default_phone_number",
                "default_street_address1",
                "default_street_address2",
                "default_town_or_city",
                "default_county",
                "default_postcode",
                "default_country",
            ]
        )

        placeholders = {
            "name": "Name",
            "default_phone_number": "Phone Number",
            "default_postcode": "Postal Code",
            "default_town_or_city": "Town or City",
            "default_street_address1": "Street Address 1",
            "default_street_address2": "Street Address 2",
            "default_county": "County, State or Locality",
        }

        for field in self.fields:
            if field != "default_country":
                if self.fields[field].required:
                    placeholder = f"{placeholders[field]} *"
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs["placeholder"] = placeholder
            self.fields[field].widget.attrs[
                "class"
            ] = "border-black rounded-0 profile-form-input"
            self.fields[field].label = False

    def save(self, commit=True):
        """
        Override the original save method to set the user
        """
        instance = super().save(commit=False)
        if commit:
            instance.save()
            # If the 'name' field is part of the cleaned_data,
            # save it to the user instance
            if 'name' in self.cleaned_data:
                user = instance.user
                user.name = self.cleaned_data['name']
                user.save()

        return instance
