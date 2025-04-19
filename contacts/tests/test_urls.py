"""
Tests for the contacts app URLs.
"""

from django.test import SimpleTestCase
from django.urls import resolve, reverse

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


class ContactsURLsTest(SimpleTestCase):
    """Test suite for the contacts app URLs."""

    def test_contact_list_url_resolves(self):
        """Test that the contact list URL resolves to the correct view."""
        url = reverse("contacts:contact-list")
        self.assertEqual(url, "/")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, ContactListView)

    def test_contact_detail_url_resolves(self):
        """Test that the contact detail URL resolves to the correct view."""
        url = reverse("contacts:contact-detail", kwargs={"pk": 1})
        self.assertEqual(url, "/1/")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, ContactDetailView)

    def test_contact_create_url_resolves(self):
        """Test that the contact create URL resolves to the correct view."""
        url = reverse("contacts:contact-create")
        self.assertEqual(url, "/create/")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, ContactCreateView)

    def test_contact_update_url_resolves(self):
        """Test that the contact update URL resolves to the correct view."""
        url = reverse("contacts:contact-update", kwargs={"pk": 1})
        self.assertEqual(url, "/update/1/")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, ContactUpdateView)

    def test_contact_delete_url_resolves(self):
        """Test that the contact delete URL resolves to the correct view."""
        url = reverse("contacts:contact-delete", kwargs={"pk": 1})
        self.assertEqual(url, "/delete/1/")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, ContactDeleteView)

    def test_status_list_url_resolves(self):
        """Test that the status list URL resolves to the correct view."""
        url = reverse("contacts:status-list")
        self.assertEqual(url, "/statuses/")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, ContactStatusListView)

    def test_status_detail_url_resolves(self):
        """Test that the status detail URL resolves to the correct view."""
        url = reverse("contacts:status-detail", kwargs={"pk": 1})
        self.assertEqual(url, "/statuses/1/")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, ContactStatusDetailView)

    def test_status_create_url_resolves(self):
        """Test that the status create URL resolves to the correct view."""
        url = reverse("contacts:status-create")
        self.assertEqual(url, "/statuses/create/")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, ContactStatusCreateView)

    def test_status_update_url_resolves(self):
        """Test that the status update URL resolves to the correct view."""
        url = reverse("contacts:status-update", kwargs={"pk": 1})
        self.assertEqual(url, "/statuses/1/update/")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, ContactStatusUpdateView)

    def test_status_delete_url_resolves(self):
        """Test that the status delete URL resolves to the correct view."""
        url = reverse("contacts:status-delete", kwargs={"pk": 1})
        self.assertEqual(url, "/statuses/1/delete/")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, ContactStatusDeleteView)
