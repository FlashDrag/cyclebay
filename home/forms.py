from django import forms
from django.core.validators import EmailValidator


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100, validators=[EmailValidator()])
    phone = forms.CharField(max_length=15, required=False)
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
