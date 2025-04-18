from django.urls import path

from contacts.views import (
    ContactCreateView,
    ContactDeleteView,
    ContactDetailView,
    ContactListView,
    ContactUpdateView,
)

app_name = "contacts"

urlpatterns = [
    path("", ContactListView.as_view(), name="contact-list"),
    path("<int:pk>/", ContactDetailView.as_view(), name="contact-detail"),
    path("create/", ContactCreateView.as_view(), name="contact-create"),
    path("update/<int:pk>/", ContactUpdateView.as_view(), name="contact-update"),
    path("delete/<int:pk>/", ContactDeleteView.as_view(), name="contact-delete"),
]
