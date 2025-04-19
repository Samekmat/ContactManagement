from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from contacts.models import Contact
from testing.factories import ContactFactory, ContactStatusFactory, UserFactory


class ContactAPITests(APITestCase):
    """Test suite for the Contact API endpoints."""

    def setUp(self):
        """Set up test data."""
        # Create a test user
        self.user = UserFactory()

        # Create test statuses
        self.active_status = ContactStatusFactory(name="Active")
        self.archived_status = ContactStatusFactory(name="Archived")

        # Create test contacts
        self.contact1 = ContactFactory(
            first_name="John",
            last_name="Doe",
            phone_number="123456789",
            email="john@example.com",
            city="New York",
            status=self.active_status,
        )

        self.contact2 = ContactFactory(
            first_name="Jane",
            last_name="Smith",
            phone_number="987654321",
            email="jane@example.com",
            city="Los Angeles",
            status=self.active_status,
        )

        # URLs
        self.list_url = reverse("contact-list")
        self.detail_url = reverse("contact-detail", kwargs={"pk": self.contact1.pk})

        # Authenticate
        self.client.force_authenticate(user=self.user)

    def test_get_contact_list(self):
        """Test retrieving a list of contacts."""
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(len(response.data["results"]), 2)

        # Check pagination
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)

    def test_get_contact_detail(self):
        """Test retrieving a single contact."""
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "John")
        self.assertEqual(response.data["last_name"], "Doe")
        self.assertEqual(response.data["email"], "john@example.com")
        self.assertEqual(response.data["status"]["name"], "Active")

    def test_create_contact(self):
        """Test creating a new contact."""
        data = {
            "first_name": "Alice",
            "last_name": "Johnson",
            "phone_number": "555123456",
            "email": "alice@example.com",
            "city": "Chicago",
            "status_id": self.active_status.id,
        }

        response = self.client.post(self.list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 3)

        # Check the created contact
        new_contact = Contact.objects.get(email="alice@example.com")
        self.assertEqual(new_contact.first_name, "Alice")
        self.assertEqual(new_contact.status, self.active_status)

    def test_update_contact(self):
        """Test updating an existing contact."""
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "123456789",
            "email": "john@example.com",
            "city": "Boston",  # Changed city
            "status_id": self.archived_status.id,  # Changed status
        }

        response = self.client.put(self.detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh from a database
        self.contact1.refresh_from_db()
        self.assertEqual(self.contact1.city, "Boston")
        self.assertEqual(self.contact1.status, self.archived_status)

    def test_partial_update_contact(self):
        """Test partially updating a contact."""
        data = {"city": "Miami", "status_id": self.archived_status.id}

        response = self.client.patch(self.detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh from a database
        self.contact1.refresh_from_db()
        self.assertEqual(self.contact1.city, "Miami")
        self.assertEqual(self.contact1.status, self.archived_status)
        # Other fields should remain unchanged
        self.assertEqual(self.contact1.first_name, "John")
        self.assertEqual(self.contact1.last_name, "Doe")

    def test_delete_contact(self):
        """Test deleting a contact."""
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Contact.objects.count(), 1)

        # Verify the contact is deleted
        with self.assertRaises(Contact.DoesNotExist):
            Contact.objects.get(pk=self.contact1.pk)

    def test_filter_contacts_by_status(self):
        """Test filtering contacts by status."""
        # Create a contact with different status
        ContactFactory(
            first_name="Bob",
            last_name="Brown",
            phone_number="111222333",
            email="bob@example.com",
            city="Dallas",
            status=self.archived_status,
        )

        # Filter by active status
        response = self.client.get(f"{self.list_url}?status={self.active_status.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)

        # Filter by archived status
        response = self.client.get(f"{self.list_url}?status={self.archived_status.id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["first_name"], "Bob")

    def test_filter_contacts_by_city(self):
        """Test filtering contacts by city."""
        response = self.client.get(f"{self.list_url}?city=New York")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["first_name"], "John")

    def test_search_contacts(self):
        """Test searching contacts."""
        # Search by first name
        response = self.client.get(f"{self.list_url}?search=John")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["first_name"], "John")

        # Search by email
        response = self.client.get(f"{self.list_url}?search=jane@example.com")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["first_name"], "Jane")

    def test_order_contacts(self):
        """Test ordering contacts."""
        # Order by last_name
        response = self.client.get(f"{self.list_url}?ordering=last_name")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["last_name"], "Doe")
        self.assertEqual(response.data["results"][1]["last_name"], "Smith")

        # Order by last_name descending
        response = self.client.get(f"{self.list_url}?ordering=-last_name")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["last_name"], "Smith")
        self.assertEqual(response.data["results"][1]["last_name"], "Doe")

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

        # Try to create a contact
        data = {
            "first_name": "Unauthorized",
            "last_name": "User",
            "phone_number": "999888777",
            "email": "unauthorized@example.com",
            "city": "Unknown",
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
