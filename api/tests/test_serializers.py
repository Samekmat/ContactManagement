from django.test import TestCase

from api.serializers import ContactSerializer, ContactStatusSerializer
from contacts.models import Contact
from testing.factories import ContactFactory, ContactStatusFactory


class ContactStatusSerializerTests(TestCase):
    """Test suite for the ContactStatusSerializer."""

    def setUp(self):
        """Set up test data."""
        self.status = ContactStatusFactory(name="Active")
        self.serializer = ContactStatusSerializer(instance=self.status)

    def test_contains_expected_fields(self):
        """Test that the serializer contains the expected fields."""
        data = self.serializer.data
        self.assertEqual(set(data.keys()), {"id", "name"})

    def test_name_field_content(self):
        """Test that the name field contains the correct data."""
        data = self.serializer.data
        self.assertEqual(data["name"], "Active")


class ContactSerializerTests(TestCase):
    """Test suite for the ContactSerializer."""

    def setUp(self):
        """Set up test data."""
        self.status = ContactStatusFactory(name="Active")
        self.contact = ContactFactory(
            first_name="John",
            last_name="Doe",
            phone_number="123456789",
            email="john@example.com",
            city="New York",
            status=self.status,
        )
        self.serializer = ContactSerializer(instance=self.contact)

    def test_contains_expected_fields(self):
        """Test that the serializer contains the expected fields."""
        data = self.serializer.data
        expected_fields = {"id", "first_name", "last_name", "phone_number", "email", "city", "status", "created_at"}
        self.assertEqual(set(data.keys()), expected_fields)
        # status_id is write-only, so it shouldn't be in the output data

    def test_status_field_content(self):
        """Test that the status field contains the correct nested data."""
        data = self.serializer.data
        self.assertEqual(data["status"]["name"], "Active")
        self.assertEqual(data["status"]["id"], self.status.id)

    def test_create_contact_with_status_id(self):
        """Test creating a contact with status_id."""
        new_status = ContactStatusFactory(name="Potential")
        data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "phone_number": "987654321",
            "email": "jane@example.com",
            "city": "Los Angeles",
            "status_id": new_status.id,
        }
        serializer = ContactSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        contact = serializer.save()
        self.assertEqual(contact.status, new_status)

    def test_update_contact_with_status_id(self):
        """Test updating a contact's status with status_id."""
        new_status = ContactStatusFactory(name="Archived")
        data = {
            "status_id": new_status.id,
        }
        serializer = ContactSerializer(instance=self.contact, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        contact = serializer.save()
        self.assertEqual(contact.status, new_status)

    def test_validation_error_on_invalid_email(self):
        """Test that the serializer validates email format."""
        data = {
            "first_name": "Invalid",
            "last_name": "Email",
            "phone_number": "123456789",
            "email": "not-an-email",
            "city": "Test City",
            "status_id": self.status.id,
        }
        serializer = ContactSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
