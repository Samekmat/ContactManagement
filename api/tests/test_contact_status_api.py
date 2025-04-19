from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from contacts.models import ContactStatusChoices
from testing.factories import ContactStatusFactory, UserFactory


class ContactStatusAPITests(APITestCase):
    """Test suite for the Contact Status API endpoints."""

    def setUp(self):
        """Set up test data."""
        # Create a test user
        self.user = UserFactory()

        # Create test statuses
        self.active_status = ContactStatusFactory(name="Active")
        self.archived_status = ContactStatusFactory(name="Archived")
        self.potential_status = ContactStatusFactory(name="Potential")

        # URLs
        self.list_url = reverse("status-list")
        self.detail_url = reverse("status-detail", kwargs={"pk": self.active_status.pk})

        # Authenticate
        self.client.force_authenticate(user=self.user)

    def test_get_status_list(self):
        """Test retrieving a list of contact statuses."""
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 3)
        self.assertEqual(len(response.data["results"]), 3)

        # Check pagination
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)

        # Check status names are in the response
        status_names = [status_obj["name"] for status_obj in response.data["results"]]
        self.assertIn("Active", status_names)
        self.assertIn("Archived", status_names)
        self.assertIn("Potential", status_names)

    def test_get_status_detail(self):
        """Test retrieving a single contact status."""
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Active")
        self.assertEqual(response.data["id"], self.active_status.id)

    def test_create_status_not_allowed(self):
        """Test that creating a status is not allowed (read-only ViewSet)."""
        data = {"name": "New Status"}

        response = self.client.post(self.list_url, data)

        # Should return 405 Method Not Allowed
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # Verify no new status was created
        self.assertEqual(ContactStatusChoices.objects.count(), 3)

    def test_update_status_not_allowed(self):
        """Test that updating a status is not allowed (read-only ViewSet)."""
        data = {"name": "Updated Status"}

        response = self.client.put(self.detail_url, data)

        # Should return 405 Method Not Allowed
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # Verify status was not updated
        self.active_status.refresh_from_db()
        self.assertEqual(self.active_status.name, "Active")

    def test_delete_status_not_allowed(self):
        """Test that deleting a status is not allowed (read-only ViewSet)."""
        response = self.client.delete(self.detail_url)

        # Should return 405 Method Not Allowed
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # Verify status was not deleted
        self.assertEqual(ContactStatusChoices.objects.count(), 3)

    def test_unauthenticated_access(self):
        """Test that unauthenticated users cannot access the API."""
        # Logout
        self.client.force_authenticate(user=None)

        # Try to access the list endpoint
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Try to access the detail endpoint
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
