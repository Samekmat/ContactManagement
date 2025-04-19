"""
Factories for creating test objects.

This module provides factory classes for creating test objects in a DRY way.
These factories can be used by all apps in the project for testing.
"""

import factory
from django.contrib.auth.models import User

from contacts.models import Contact, ContactStatusChoices


class UserFactory(factory.django.DjangoModelFactory):
    """Factory for creating User instances."""

    class Meta:
        """Metaclass for UserFactory defining model and get_or_create behavior."""

        model = User
        django_get_or_create = ("username",)

    username = factory.Sequence(lambda n: f"testuser{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "testpassword")


class ContactStatusFactory(factory.django.DjangoModelFactory):
    """Factory for creating ContactStatusChoices instances."""

    class Meta:
        """Metaclass for ContactStatusFactory defining model and get_or_create behavior."""

        model = ContactStatusChoices
        django_get_or_create = ("name",)

    name = factory.Sequence(lambda n: f"Status {n}")


class ContactFactory(factory.django.DjangoModelFactory):
    """Factory for creating Contact instances."""

    class Meta:
        """Metaclass for ContactFactory defining model and get_or_create behavior."""

        model = Contact
        django_get_or_create = ("email",)

    first_name = factory.Sequence(lambda n: f"First{n}")
    last_name = factory.Sequence(lambda n: f"Last{n}")
    phone_number = factory.Sequence(lambda n: f"{n:09d}")  # 9-digit number with leading zeros
    email = factory.LazyAttribute(lambda obj: f"{obj.first_name.lower()}.{obj.last_name.lower()}@example.com")
    city = factory.Sequence(lambda n: f"City{n}")
    status = factory.SubFactory(ContactStatusFactory, name="Active")
