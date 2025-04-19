from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from contacts.forms import ContactForm, StatusForm
from contacts.models import Contact, ContactStatusChoices


class ContactListView(LoginRequiredMixin, ListView):
    """Displays a paginated list of Contact objects with optional filtering, sorting and searching."""

    model = Contact
    template_name = "contacts/contact_list.html"
    context_object_name = "contacts"
    paginate_by = 5

    def get_ordering(self: "ContactListView") -> str:
        """
        Determine the ordering of the queryset based on the request GET parameters.

        :return:
            str: A string indicating the field to order by defaults to "last_name".
        """
        ordering = self.request.GET.get("sort", "last_name")
        if ordering not in ["last_name", "-last_name", "created_at", "-created_at"]:
            ordering = "last_name"
        return ordering

    def get_queryset(self: "ContactListView"):
        """
        Return a filtered queryset based on the search query and ordering.

        :return:
            QuerySet: Filtered and ordered queryset.
        """
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        status = self.request.GET.get("status")

        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
                | Q(email__icontains=query)
                | Q(phone_number__icontains=query)
                | Q(city__icontains=query),
            )

        if status and status.isdigit():
            queryset = queryset.filter(status_id=int(status))

        return queryset.order_by(self.get_ordering())

    def get_context_data(self: "ContactListView", **kwargs: dict) -> dict:
        """
        Add additional context data to the template.

        :param kwargs: Keyword arguments passed to the context.

        :return:
            dict: The context dictionary with the current sort order and search query.
        """
        context = super().get_context_data(**kwargs)
        context["current_sort"] = self.request.GET.get("sort", "last_name")
        context["query"] = self.request.GET.get("q", "")
        context["current_status"] = self.request.GET.get("status", "")
        context["statuses"] = ContactStatusChoices.objects.all()
        return context


class ContactDetailView(LoginRequiredMixin, DetailView):
    """Displays detailed information about a specific contact."""

    model = Contact
    template_name = "contacts/contact_detail.html"
    context_object_name = "contact"


class ContactCreateView(LoginRequiredMixin, CreateView):
    """Provides a form for creating a new contact."""

    model = Contact
    form_class = ContactForm
    template_name = "contacts/contact_form.html"
    success_url = reverse_lazy("contacts:contact-list")


class ContactUpdateView(LoginRequiredMixin, UpdateView):
    """Provides a form for editing an existing contact."""

    model = Contact
    form_class = ContactForm
    template_name = "contacts/contact_form.html"
    success_url = reverse_lazy("contacts:contact-list")


class ContactDeleteView(LoginRequiredMixin, DeleteView):
    """Asks for confirmation and deletes a selected contact."""

    model = Contact
    template_name = "contacts/contact_confirm_delete.html"
    success_url = reverse_lazy("contacts:contact-list")


class ContactStatusListView(LoginRequiredMixin, ListView):
    """Displays a list of all contact status choices."""

    model = ContactStatusChoices
    template_name = "statuses/contact_status_choices_list.html"
    context_object_name = "statuses"


class ContactStatusDetailView(LoginRequiredMixin, DetailView):
    """Displays details of a specific contact status."""

    model = ContactStatusChoices
    template_name = "statuses/contact_status_choices_detail.html"
    context_object_name = "status"


class ContactStatusCreateView(LoginRequiredMixin, CreateView):
    """Provides a form for creating a new contact status."""

    model = ContactStatusChoices
    form_class = StatusForm
    template_name = "statuses/contact_status_choices_form.html"
    success_url = reverse_lazy("contacts:status-list")


class ContactStatusUpdateView(LoginRequiredMixin, UpdateView):
    """Provides a form for updating an existing contact status."""

    model = ContactStatusChoices
    form_class = StatusForm
    template_name = "statuses/contact_status_choices_form.html"
    success_url = reverse_lazy("contacts:status-list")


class ContactStatusDeleteView(LoginRequiredMixin, DeleteView):
    """Asks for confirmation and deletes a contact status."""

    model = ContactStatusChoices
    template_name = "statuses/contact_status_choices_confirm_delete.html"
    success_url = reverse_lazy("contacts:status-list")
