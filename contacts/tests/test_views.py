"""
Tests for the contacts app views.
"""

from django.test import TestCase
from django.urls import reverse

from contacts.models import Contact, ContactStatusChoices
from testing.factories import ContactFactory, ContactStatusFactory, UserFactory


class ContactViewsTest(TestCase):
    """Test suite for the Contact views."""

    def setUp(self):
        """Set up test data."""
        # Create a test user
        self.user = UserFactory()
        self.client.force_login(self.user)

        # Create test statuses
        self.active_status = ContactStatusFactory(name="Active")
        self.archived_status = ContactStatusFactory(name="Archived")

        # Create test contacts
        self.contact1 = ContactFactory(
            first_name="John",
            last_name="Doe",
            phone_number="123456789",
            email="john.doe@example.com",
            city="New York",
            status=self.active_status,
        )
        self.contact2 = ContactFactory(
            first_name="Jane",
            last_name="Smith",
            phone_number="987654321",
            email="jane.smith@example.com",
            city="Los Angeles",
            status=self.active_status,
        )

        # URLs
        self.list_url = reverse("contacts:contact-list")
        self.detail_url = reverse("contacts:contact-detail", kwargs={"pk": self.contact1.pk})
        self.create_url = reverse("contacts:contact-create")
        self.update_url = reverse("contacts:contact-update", kwargs={"pk": self.contact1.pk})
        self.delete_url = reverse("contacts:contact-delete", kwargs={"pk": self.contact1.pk})

    def test_contact_list_view(self):
        """Test the contact list view."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contacts/contact_list.html")
        self.assertContains(response, "John Doe")
        self.assertContains(response, "Jane Smith")

    def test_contact_detail_view(self):
        """Test the contact detail view."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contacts/contact_detail.html")
        self.assertContains(response, "John Doe")
        self.assertContains(response, "john.doe@example.com")

    def test_contact_create_view(self):
        """Test the contact create view."""
        # Test GET request
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contacts/contact_form.html")

        # Test POST request
        data = {
            "first_name": "Alice",
            "last_name": "Johnson",
            "phone_number": "555123456",
            "email": "alice.johnson@example.com",
            "city": "Chicago",
            "status": self.active_status.id,
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertRedirects(response, self.list_url)

        # Verify the contact was created
        self.assertTrue(Contact.objects.filter(email="alice.johnson@example.com").exists())

    def test_contact_update_view(self):
        """Test the contact update view."""
        # Test GET request
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contacts/contact_form.html")

        # Test POST request
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "123456789",
            "email": "john.doe@example.com",
            "city": "Boston",  # Changed city
            "status": self.archived_status.id,  # Changed status
        }
        response = self.client.post(self.update_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.assertRedirects(response, self.list_url)

        # Verify the contact was updated
        self.contact1.refresh_from_db()
        self.assertEqual(self.contact1.city, "Boston")
        self.assertEqual(self.contact1.status, self.archived_status)

    def test_contact_delete_view(self):
        """Test the contact delete view."""
        # Test GET request (confirmation page)
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contacts/contact_confirm_delete.html")

        # Test POST request (actual deletion)
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertRedirects(response, self.list_url)

        # Verify the contact was deleted
        self.assertFalse(Contact.objects.filter(pk=self.contact1.pk).exists())

    def test_contact_list_search(self):
        """Test the contact list search functionality."""
        # Search by first name
        response = self.client.get(f"{self.list_url}?q=John")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John Doe")
        self.assertNotContains(response, "Jane Smith")

        # Search by email
        response = self.client.get(f"{self.list_url}?q=jane.smith")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Jane Smith")
        self.assertNotContains(response, "John Doe")

    def test_contact_list_filter_by_status(self):
        """Test the contact list filter by status functionality."""
        # Create a contact with different status
        ContactFactory(
            first_name="Bob",
            last_name="Brown",
            phone_number="111222333",
            email="bob.brown@example.com",
            city="Dallas",
            status=self.archived_status,
        )

        # Filter by active status
        response = self.client.get(f"{self.list_url}?status={self.active_status.id}")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John Doe")
        self.assertContains(response, "Jane Smith")
        self.assertNotContains(response, "Bob Brown")

        # Filter by archived status
        response = self.client.get(f"{self.list_url}?status={self.archived_status.id}")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bob Brown")
        self.assertNotContains(response, "John Doe")
        self.assertNotContains(response, "Jane Smith")

    def test_contact_list_sorting(self):
        """Test the contact list sorting functionality."""
        # Sort by last name (default)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        # Check that Doe comes before Smith in the content
        self.assertTrue(content.find("Doe") < content.find("Smith"))

        # Sort by last name descending
        response = self.client.get(f"{self.list_url}?sort=-last_name")
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        # Check that Smith comes before Doe in the content
        self.assertTrue(content.find("Smith") < content.find("Doe"))

    def test_unauthenticated_access(self):
        """Test that unauthenticated users are redirected to login."""
        # Logout
        self.client.logout()

        # Try to access the list view
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(response.url.startswith("/accounts/login/"))

        # Try to access the detail view
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(response.url.startswith("/accounts/login/"))


class ContactStatusViewsTest(TestCase):
    """Test suite for the ContactStatus views."""

    def setUp(self):
        """Set up test data."""
        # Create a test user
        self.user = UserFactory()
        self.client.force_login(self.user)

        # Create test statuses
        self.active_status = ContactStatusFactory(name="Active")
        self.archived_status = ContactStatusFactory(name="Archived")

        # URLs
        self.list_url = reverse("contacts:status-list")
        self.detail_url = reverse("contacts:status-detail", kwargs={"pk": self.active_status.pk})
        self.create_url = reverse("contacts:status-create")
        self.update_url = reverse("contacts:status-update", kwargs={"pk": self.active_status.pk})
        self.delete_url = reverse("contacts:status-delete", kwargs={"pk": self.active_status.pk})

    def test_status_list_view(self):
        """Test the status list view."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "statuses/contact_status_choices_list.html")
        self.assertContains(response, "Active")
        self.assertContains(response, "Archived")

    def test_status_detail_view(self):
        """Test the status detail view."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "statuses/contact_status_choices_detail.html")
        self.assertContains(response, "Active")

    def test_status_create_view(self):
        """Test the status create view."""
        # Test GET request
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "statuses/contact_status_choices_form.html")

        # Test POST request
        data = {"name": "New Status"}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertRedirects(response, self.list_url)

        # Verify the status was created
        self.assertTrue(ContactStatusChoices.objects.filter(name="New Status").exists())

    def test_status_update_view(self):
        """Test the status update view."""
        # Test GET request
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "statuses/contact_status_choices_form.html")

        # Test POST request
        data = {"name": "Updated Status"}
        response = self.client.post(self.update_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.assertRedirects(response, self.list_url)

        # Verify the status was updated
        self.active_status.refresh_from_db()
        self.assertEqual(self.active_status.name, "Updated Status")

    def test_status_delete_view(self):
        """Test the status delete view."""
        # Test GET request (confirmation page)
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "statuses/contact_status_choices_confirm_delete.html")

        # Test POST request (actual deletion)
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertRedirects(response, self.list_url)

        # Verify the status was deleted
        self.assertFalse(ContactStatusChoices.objects.filter(pk=self.active_status.pk).exists())

    def test_unauthenticated_access(self):
        """Test that unauthenticated users are redirected to login."""
        # Logout
        self.client.logout()

        # Try to access the list view
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(response.url.startswith("/accounts/login/"))

        # Try to access the detail view
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(response.url.startswith("/accounts/login/"))
