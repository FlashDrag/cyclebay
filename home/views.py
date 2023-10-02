from django.shortcuts import render


def home(request):
    return render(request, "home/index.html")


def privacy(request):
    return render(request, "home/privacy.html")
