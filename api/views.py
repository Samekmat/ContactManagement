from typing import ClassVar

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from api.serializers import ContactSerializer, ContactStatusSerializer
from contacts.models import Contact, ContactStatusChoices


class ContactViewSet(viewsets.ModelViewSet):
    queryset: ClassVar[Contact.objects.all()] = Contact.objects.all()
    serializer_class = ContactSerializer
    filter_backends: ClassVar[list] = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields: ClassVar[list] = ["status", "city"]
    search_fields: ClassVar[list] = ["first_name", "last_name", "email"]
    ordering_fields: ClassVar[list] = ["created_at", "last_name"]


class ContactStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset: ClassVar[ContactStatusChoices.objects.all()] = ContactStatusChoices.objects.all()
    serializer_class = ContactStatusSerializer
