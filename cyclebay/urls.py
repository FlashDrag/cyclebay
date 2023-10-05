from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .views import (
    custom_bad_request_view,
    custom_permission_denied_view,
    custom_page_not_found_view,
    custom_server_error_view,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("home.urls")),
    path("products/", include("inventorize.urls")),
    path("products/", include("products.urls")),
    path('bag/', include('bag.urls')),
    path('checkout/', include('checkout.urls')),
    path('profile/', include('profiles.urls')),
    path('wishlist/', include('wishlist.urls')),
    #  allows to serve media files in development
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler400 = custom_bad_request_view
handler403 = custom_permission_denied_view
handler404 = custom_page_not_found_view
handler500 = custom_server_error_view
