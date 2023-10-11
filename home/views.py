from django.shortcuts import redirect, render
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail

from products.models import Product

from .forms import ContactForm


def home(request):
    featured = Product.objects.filter(featured=True)[:8]

    context = {
        "featured": featured,
    }
    return render(request, "home/index.html", context)


def privacy(request):
    return render(request, "home/privacy.html")


def shipping(request):
    return render(request, "home/shipping.html")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            message = (
                f"Contact Form Message\n\n"
                f"Name: {form.cleaned_data['name']}\n"
                f"Phone: {form.cleaned_data['phone']}\n"
                f"From Email: {form.cleaned_data['email']}\n\n"
                f"{form.cleaned_data['message']}"
            )
            # send email to store owner
            send_mail(
                subject=form.cleaned_data["subject"],
                message=message,
                from_email=form.cleaned_data["email"],
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            messages.info(
                request,
                "Thank you for your message. We will get back to you soon.",
            )
            return redirect("home")
    else:
        # if user is authenticated, prefill the form with their email and name
        if request.user.is_authenticated:
            form = ContactForm(
                initial={
                    "name": request.user.name,
                    "email": request.user.email,
                }
            )
        else:
            form = ContactForm()
    return render(request, "home/contact.html", {"form": form})
