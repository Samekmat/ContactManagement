from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.forms import Form
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from .forms import RegistrationForm


class RegisterView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self: "RegisterView", form: Form) -> HttpResponse:
        """Handle the form submission and log the user in after registration."""
        response = super().form_valid(form)
        login(self.request, self.object)
        return redirect("index", response=response)


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"
