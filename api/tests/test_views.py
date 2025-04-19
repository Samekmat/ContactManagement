from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate

from api.views import ContactStatusViewSet, ContactViewSet
from contacts.models import Contact
from testing.factories import ContactFactory, ContactStatusFactory, UserFactory


class ContactViewSetTests(TestCase):
    """Test suite for the ContactViewSet."""

    def setUp(self):
        """Set up test data."""
        self.factory = APIRequestFactory()
        self.user = UserFactory()
        self.active_status = ContactStatusFactory(name="Active")
        self.archived_status = ContactStatusFactory(name="Archived")

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

    def test_list_contacts(self):
        """Test that the view returns a list of contacts."""
        request = self.factory.get(reverse("contact-list"))
        force_authenticate(request, user=self.user)
        view = ContactViewSet.as_view({"get": "list"})
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)

    def test_retrieve_contact(self):
        """Test that the view returns a single contact."""
        request = self.factory.get(reverse("contact-detail", kwargs={"pk": self.contact1.pk}))
        force_authenticate(request, user=self.user)
        view = ContactViewSet.as_view({"get": "retrieve"})
        response = view(request, pk=self.contact1.pk)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["first_name"], "John")
        self.assertEqual(response.data["last_name"], "Doe")

    def test_create_contact(self):
        """Test creating a contact through the view."""
        data = {
            "first_name": "Alice",
            "last_name": "Johnson",
            "phone_number": "555123456",
            "email": "alice@example.com",
            "city": "Chicago",
            "status_id": self.active_status.id,
        }
        request = self.factory.post(reverse("contact-list"), data)
        force_authenticate(request, user=self.user)
        view = ContactViewSet.as_view({"post": "create"})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Contact.objects.count(), 3)
        self.assertEqual(Contact.objects.get(email="alice@example.com").first_name, "Alice")

    def test_update_contact(self):
        """Test updating a contact through the view."""
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "123456789",
            "email": "john@example.com",
            "city": "Boston",
            "status_id": self.archived_status.id,
        }
        request = self.factory.put(reverse("contact-detail", kwargs={"pk": self.contact1.pk}), data)
        force_authenticate(request, user=self.user)
        view = ContactViewSet.as_view({"put": "update"})
        response = view(request, pk=self.contact1.pk)

        self.assertEqual(response.status_code, 200)
        self.contact1.refresh_from_db()
        self.assertEqual(self.contact1.city, "Boston")
        self.assertEqual(self.contact1.status, self.archived_status)

    def test_filter_by_status(self):
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

        request = self.factory.get(f"{reverse('contact-list')}?status={self.archived_status.id}")
        force_authenticate(request, user=self.user)
        view = ContactViewSet.as_view({"get": "list"})
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["first_name"], "Bob")


class ContactStatusViewSetTests(TestCase):
    """Test suite for the ContactStatusViewSet."""

    def setUp(self):
        """Set up test data."""
        self.factory = APIRequestFactory()
        self.user = UserFactory()
        self.active_status = ContactStatusFactory(name="Active")
        self.archived_status = ContactStatusFactory(name="Archived")

    def test_list_statuses(self):
        """Test that the view returns a list of statuses."""
        request = self.factory.get(reverse("status-list"))
        force_authenticate(request, user=self.user)
        view = ContactStatusViewSet.as_view({"get": "list"})
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 2)

    def test_retrieve_status(self):
        """Test that the view returns a single status."""
        request = self.factory.get(reverse("status-detail", kwargs={"pk": self.active_status.pk}))
        force_authenticate(request, user=self.user)
        view = ContactStatusViewSet.as_view({"get": "retrieve"})
        response = view(request, pk=self.active_status.pk)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Active")

    def test_create_not_allowed(self):
        """Test that creating a status is not allowed."""
        data = {"name": "New Status"}
        request = self.factory.post(reverse("status-list"), data)
        force_authenticate(request, user=self.user)
        view = ContactStatusViewSet.as_view({"post": "create"})

        # ReadOnlyModelViewSet doesn't have a create method
        with self.assertRaises(AttributeError):
            response = view(request)
