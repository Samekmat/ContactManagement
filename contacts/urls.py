from django.urls import path

from contacts.views import (
    ContactCreateView,
    ContactDeleteView,
    ContactDetailView,
    ContactListView,
    ContactStatusCreateView,
    ContactStatusDeleteView,
    ContactStatusDetailView,
    ContactStatusListView,
    ContactStatusUpdateView,
    ContactUpdateView,
)

app_name = "contacts"

urlpatterns = [
    path("", ContactListView.as_view(), name="contact-list"),
    path("<int:pk>/", ContactDetailView.as_view(), name="contact-detail"),
    path("create/", ContactCreateView.as_view(), name="contact-create"),
    path("update/<int:pk>/", ContactUpdateView.as_view(), name="contact-update"),
    path("delete/<int:pk>/", ContactDeleteView.as_view(), name="contact-delete"),
    # statutes
    path("statuses/", ContactStatusListView.as_view(), name="status-list"),
    path("statuses/<int:pk>/", ContactStatusDetailView.as_view(), name="status-detail"),
    path("statuses/create/", ContactStatusCreateView.as_view(), name="status-create"),
    path("statuses/<int:pk>/update/", ContactStatusUpdateView.as_view(), name="status-update"),
    path("statuses/<int:pk>/delete/", ContactStatusDeleteView.as_view(), name="status-delete"),
]
