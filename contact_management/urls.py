from django.contrib import admin
from django.urls import include, path

from contact_management.views import IndexView, RegisterView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("contacts.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/register/", RegisterView.as_view(), name="register"),
    path("", IndexView.as_view(), name="index"),
]
