from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from django.views.generic.edit import CreateView


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy(
        "login"
    )  # Redirect to login page after successful registration
    template_name = "registration/signup.html"


User = get_user_model()


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "users/profile.html"

    def get_object(self):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["username", "email"]  # Adjust fields based on your User model
    template_name = "users/profile_edit.html"
    success_url = reverse_lazy("profile")

    def get_object(self):
        return self.request.user
