from typing import ClassVar

from django import forms

from contacts.models import Contact

POLAND_PHONE_NUMBER_LENGTH_NO_PREFIX = 9


class ContactForm(forms.ModelForm):
    """Form to create or update a contact."""

    class Meta:
        """Metadata for ContactForm."""

        model = Contact
        fields = (
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "city",
            "status",
        )
        widgets: ClassVar[dict] = {
            "first_name": forms.TextInput(
                attrs={"class": "w-full px-4 py-2 border rounded-md", "placeholder": "First name"},
            ),
            "last_name": forms.TextInput(
                attrs={"class": "w-full px-4 py-2 border rounded-md", "placeholder": "Last name"},
            ),
            "phone_number": forms.TextInput(
                attrs={"class": "w-full px-4 py-2 border rounded-md", "placeholder": "Phone number"},
            ),
            "email": forms.EmailInput(
                attrs={"class": "w-full px-4 py-2 border rounded-md", "placeholder": "Email address"},
            ),
            "city": forms.TextInput(attrs={"class": "w-full px-4 py-2 border rounded-md", "placeholder": "City"}),
            "status": forms.Select(attrs={"class": "w-full px-4 py-2 border rounded-md"}),
        }

    def clean_phone_number(self: "ContactForm") -> str:
        """Ensure the phone number length is valid."""
        phone_number = self.cleaned_data.get("phone_number")

        if len(phone_number) != POLAND_PHONE_NUMBER_LENGTH_NO_PREFIX:
            raise forms.ValidationError("Phone number must be 9 digits long.")
        return phone_number
