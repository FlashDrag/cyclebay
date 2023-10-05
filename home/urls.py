from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('privacy/', views.privacy, name='privacy'),
    path('shipping/', views.shipping, name='shipping'),
    path('contact/', views.contact, name='contact'),
]
