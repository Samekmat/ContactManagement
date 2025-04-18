from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"placeholder": "you@example.com"}))

    class Meta:
        """
        Model: Built-in User model.

        Fields: username, email, password1, password2 from the User model.
        """

        model = User
        fields = ("username", "email", "password1", "password2")
