"""
Tests for the contacts app models.
"""

from django.test import TestCase

from testing.factories import ContactFactory, ContactStatusFactory


class ContactStatusChoicesModelTest(TestCase):
    """Test suite for the ContactStatusChoices model."""

    def setUp(self):
        """Set up test data."""
        self.status = ContactStatusFactory(name="Test Status")

    def test_string_representation(self):
        """Test the string representation of a ContactStatusChoices instance."""
        self.assertEqual(str(self.status), "Test Status")

    def test_name_max_length(self):
        """Test that the name field has the correct max length."""
        max_length = self.status._meta.get_field("name").max_length
        self.assertEqual(max_length, 50)

    def test_name_unique(self):
        """Test that the name field is unique."""
        unique = self.status._meta.get_field("name").unique
        self.assertTrue(unique)


class ContactModelTest(TestCase):
    """Test suite for the Contact model."""

    def setUp(self):
        """Set up test data."""
        self.status = ContactStatusFactory(name="Active")
        self.contact = ContactFactory(
            first_name="John",
            last_name="Doe",
            phone_number="123456789",
            email="john.doe@example.com",
            city="New York",
            status=self.status,
        )

    def test_string_representation(self):
        """Test the string representation of a Contact instance."""
        self.assertEqual(str(self.contact), "John Doe")

    def test_first_name_max_length(self):
        """Test that the first_name field has the correct max length."""
        max_length = self.contact._meta.get_field("first_name").max_length
        self.assertEqual(max_length, 50)

    def test_last_name_max_length(self):
        """Test that the last_name field has the correct max length."""
        max_length = self.contact._meta.get_field("last_name").max_length
        self.assertEqual(max_length, 50)

    def test_phone_number_max_length(self):
        """Test that the phone_number field has the correct max length."""
        max_length = self.contact._meta.get_field("phone_number").max_length
        self.assertEqual(max_length, 9)

    def test_phone_number_unique(self):
        """Test that the phone_number field is unique."""
        unique = self.contact._meta.get_field("phone_number").unique
        self.assertTrue(unique)

    def test_email_max_length(self):
        """Test that the email field has the correct max length."""
        max_length = self.contact._meta.get_field("email").max_length
        self.assertEqual(max_length, 100)

    def test_email_unique(self):
        """Test that the email field is unique."""
        unique = self.contact._meta.get_field("email").unique
        self.assertTrue(unique)

    def test_city_max_length(self):
        """Test that the city field has the correct max length."""
        max_length = self.contact._meta.get_field("city").max_length
        self.assertEqual(max_length, 50)

    def test_status_optional(self):
        """Test that the status field is optional."""
        contact = ContactFactory(status=None)
        self.assertIsNone(contact.status)

    def test_created_at_auto_now_add(self):
        """Test that the created_at field is set automatically."""
        self.assertIsNotNone(self.contact.created_at)
