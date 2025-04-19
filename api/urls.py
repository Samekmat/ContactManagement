from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ContactStatusViewSet, ContactViewSet

router = DefaultRouter()
router.register(r"contacts", ContactViewSet, basename="contact")
router.register(r"statuses", ContactStatusViewSet, basename="status")

urlpatterns = [
    path("", include(router.urls)),
]
