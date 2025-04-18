from django.db import models


class ContactStatusChoices(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self: "ContactStatusChoices") -> str:
        """:return: name of the contact status"""
        return self.name
