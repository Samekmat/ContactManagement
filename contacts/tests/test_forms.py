"""
Tests for the contact app forms.
"""

from django.test import TestCase

from contacts.forms import ContactForm, StatusForm
from testing.factories import ContactStatusFactory


class ContactFormTest(TestCase):
    """Test suite for the ContactForm."""

    def setUp(self):
        """Set up test data."""
        self.status = ContactStatusFactory(name="Active")
        self.valid_data = {
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "123456789",
            "email": "john.doe@example.com",
            "city": "New York",
            "status": self.status.id,
        }

    def test_valid_form(self):
        """Test that the form is valid with correct data."""
        form = ContactForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_invalid_phone_number_length(self):
        """Test that the form is invalid with an incorrect phone number length."""
        # Test with a phone number that's too short
        data = self.valid_data.copy()
        data["phone_number"] = "12345678"  # 8 digits instead of 9
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("phone_number", form.errors)
        self.assertEqual(form.errors["phone_number"][0], "Phone number must be 9 digits long.")

        # Test with a phone number that's too long
        data = self.valid_data.copy()
        data["phone_number"] = "1234567890"  # 10 digits instead of 9
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("phone_number", form.errors)
        # Django's max_length validation kicks in before our custom validation
        self.assertEqual(form.errors["phone_number"][0], "Ensure this value has at most 9 characters (it has 10).")

    def test_required_fields(self):
        """Test that required fields are enforced."""
        required_fields = ["first_name", "last_name", "phone_number", "email", "city"]

        for field in required_fields:
            data = self.valid_data.copy()
            data[field] = ""
            form = ContactForm(data=data)
            self.assertFalse(form.is_valid())
            self.assertIn(field, form.errors)

    def test_status_optional(self):
        """Test that the status field is optional."""
        data = self.valid_data.copy()
        data.pop("status")
        form = ContactForm(data=data)
        self.assertTrue(form.is_valid())


class StatusFormTest(TestCase):
    """Test suite for the StatusForm."""

    def setUp(self):
        """Set up test data."""
        self.valid_data = {
            "name": "New Status",
        }

    def test_valid_form(self):
        """Test that the form is valid with correct data."""
        form = StatusForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_required_fields(self):
        """Test that required fields are enforced."""
        data = self.valid_data.copy()
        data["name"] = ""
        form = StatusForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_name_max_length(self):
        """Test that the name field has the correct max length."""
        data = self.valid_data.copy()
        data["name"] = "A" * 51  # 51 characters, max is 50
        form = StatusForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
