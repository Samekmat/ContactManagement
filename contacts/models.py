from django.db import models


class ContactStatusChoices(models.Model):
    """
    Model representing possible statuses for a contact.

    Each status has a unique name (e.g. 'Active', 'Archived', 'Potential').
    """

    name = models.CharField(max_length=50, unique=True)

    def __str__(self: "ContactStatusChoices") -> str:
        """:return: name of the contact status"""
        return self.name


class Contact(models.Model):
    """
    Model representing a contact person.

    Contains personal details such as name, phone, email, city,
    and a foreign key to a contact status.
    """

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=9, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    city = models.CharField(max_length=50)
    status = models.ForeignKey(
        ContactStatusChoices,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="Optional status selected from predefined choices.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self: "Contact") -> str:
        """:return: name combined of the first name and last name of the contact"""
        return f"{self.first_name} {self.last_name}"
