from django.db import models


class ContactStatusChoices(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self: "ContactStatusChoices") -> str:
        """:return: name of the contact status"""
        return self.name


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=100, unique=True)
    city = models.CharField(max_length=50)
    status = models.ForeignKey(ContactStatusChoices, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self: "Contact") -> str:
        """:return: name combined of the first name and last name of the contact"""
        return f"{self.first_name} {self.last_name}"
