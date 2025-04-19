"""
Tests for the API app URLs.
"""

from django.test import SimpleTestCase
from django.urls import resolve, reverse
from rest_framework.routers import DefaultRouter

from api.views import ContactStatusViewSet, ContactViewSet


class APIURLsTest(SimpleTestCase):
    """Test suite for the API app URLs."""

    def test_contact_list_url_resolves(self):
        """Test that the contact list URL resolves to the correct view."""
        url = reverse("contact-list")
        self.assertEqual(url, "/api/contacts/")
        resolver = resolve(url)
        self.assertEqual(resolver.func.cls, ContactViewSet, "URL should resolve to ContactViewSet")

    def test_contact_detail_url_resolves(self):
        """Test that the contact detail URL resolves to the correct view."""
        url = reverse("contact-detail", kwargs={"pk": 1})
        self.assertEqual(url, "/api/contacts/1/")
        resolver = resolve(url)
        self.assertEqual(resolver.func.cls, ContactViewSet, "URL should resolve to ContactViewSet")

    def test_status_list_url_resolves(self):
        """Test that the status list URL resolves to the correct view."""
        url = reverse("status-list")
        self.assertEqual(url, "/api/statuses/")
        resolver = resolve(url)
        self.assertEqual(resolver.func.cls, ContactStatusViewSet, "URL should resolve to ContactStatusViewSet")

    def test_status_detail_url_resolves(self):
        """Test that the status detail URL resolves to the correct view."""
        url = reverse("status-detail", kwargs={"pk": 1})
        self.assertEqual(url, "/api/statuses/1/")
        resolver = resolve(url)
        self.assertEqual(resolver.func.cls, ContactStatusViewSet, "URL should resolve to ContactStatusViewSet")

    def test_router_urls(self):
        """Test that the router generates the expected URLs."""
        router = DefaultRouter()
        router.register(r"contacts", ContactViewSet, basename="contact")
        router.register(r"statuses", ContactStatusViewSet, basename="status")

        # Check that all expected URL patterns are generated
        url_patterns = router.urls
        url_names = [pattern.name for pattern in url_patterns if hasattr(pattern, "name")]

        # For ContactViewSet (ModelViewSet)
        self.assertIn("contact-list", url_names)
        self.assertIn("contact-detail", url_names)

        # For ContactStatusViewSet (ReadOnlyModelViewSet)
        self.assertIn("status-list", url_names)
        self.assertIn("status-detail", url_names)

        # API root should also be present
        self.assertIn("api-root", url_names)
