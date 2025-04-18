from django.contrib import admin

from contacts.models import Contact, ContactStatusChoices

admin.site.register(Contact)
admin.site.register(ContactStatusChoices)
