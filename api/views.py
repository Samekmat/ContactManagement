from typing import ClassVar

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from api.serializers import ContactSerializer, ContactStatusSerializer
from contacts.models import Contact, ContactStatusChoices


class ContactViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows full CRUD operations on Contact instances.

    Features:
    - Supports filtering by `status` and `city`
    - Supports searching by `first_name`, `last_name`, and `email`
    - Supports ordering by `created_at` and `last_name`
    - Returns full contact info including nested status details
    - Accepts `status_id` for creating and updating status field

    Requires authentication.
    """

    queryset: ClassVar[Contact.objects.all()] = Contact.objects.all()
    serializer_class = ContactSerializer
    filter_backends: ClassVar[list] = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields: ClassVar[list] = ["status", "city"]
    search_fields: ClassVar[list] = ["first_name", "last_name", "email"]
    ordering_fields: ClassVar[list] = ["created_at", "last_name"]


class ContactStatusViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for listing all available contact statuses.

    This view is read-only and does not allow creating, updating, or deleting statuses.
    """

    queryset: ClassVar[ContactStatusChoices.objects.all()] = ContactStatusChoices.objects.all()
    serializer_class = ContactStatusSerializer
