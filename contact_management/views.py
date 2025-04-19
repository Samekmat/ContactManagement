from django.contrib.auth import login
from django.contrib.auth.models import User
from django.forms import Form
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import RegistrationForm


class RegisterView(CreateView):
    """
    View responsible for user registration.

    Uses a custom registration form and logs the user in immediately after
    successful registration, redirecting to the contact list view.
    """

    model = User
    form_class = RegistrationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self: "RegisterView", form: Form) -> HttpResponse:
        """Handle the form submission and log the user in after registration."""
        super().form_valid(form)
        login(self.request, self.object)
        return redirect("contact-list")
