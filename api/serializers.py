from rest_framework import serializers

from contacts.models import Contact, ContactStatusChoices


class ContactStatusSerializer(serializers.ModelSerializer):
    class Meta:
        """Metaclass for ContactStatusSerializer."""

        model = ContactStatusChoices
        fields = ["id", "name"]  # noqa: RUF012


class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer for the Contact model including related status data.

    - `status` is a nested, read-only representation of the contact's status.
    - `status_id` is a write-only field that maps to the foreign key `status`.
      Use this to assign a status when creating or updating a contact.
    """

    status = ContactStatusSerializer(read_only=True)
    status_id = serializers.PrimaryKeyRelatedField(
        queryset=ContactStatusChoices.objects.all(),
        source="status",
        write_only=True,
        required=False,
    )

    class Meta:
        """Metaclass for ContactSerializer containing additional contact status data."""

        model = Contact
        fields = [  # noqa: RUF012
            "id",
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "city",
            "status",
            "status_id",
            "created_at",
        ]
