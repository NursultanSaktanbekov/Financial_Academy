from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import logout
from django.shortcuts import redirect

from apps.academy.models import Contact
from .forms import UserLoginForm


class UserLoginView(LoginView):
    template_name = "account/login.html"
    form_class = UserLoginForm
    success_url = reverse_lazy("journal/journal_list.html")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        displayed_contacts = Contact.objects.filter(is_displayed=True)
        context["displayed_contacts"] = displayed_contacts
        return context


class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse_lazy("index"))
