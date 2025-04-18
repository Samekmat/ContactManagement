from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from contacts.forms import ContactForm
from contacts.models import Contact


class ContactListView(ListView):
    """Displays a paginated list of Contact objects with optional sorting."""

    model = Contact
    template_name = "contacts/contact_list.html"
    context_object_name = "contacts"
    paginate_by = 10

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

    def get_context_data(self: "ContactListView", **kwargs: dict) -> dict:
        """
        Add additional context data to the template.

        :param kwargs: Keyword arguments passed to the context.

        :return:
            dict: The context dictionary with the current sort order appended.
        """
        context = super().get_context_data(**kwargs)
        context["current_sort"] = self.request.GET.get("sort", "last_name")
        return context


class ContactDetailView(DetailView):
    model = Contact
    template_name = "contacts/contact_detail.html"
    context_object_name = "contact"


class ContactCreateView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "contacts/contact_form.html"
    success_url = reverse_lazy("contacts:contact-list")


class ContactUpdateView(UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = "contacts/contact_form.html"
    success_url = reverse_lazy("contacts:contact-list")


class ContactDeleteView(DeleteView):
    model = Contact
    template_name = "contacts/contact_confirm_delete.html"
    success_url = reverse_lazy("contacts:contact-list")
