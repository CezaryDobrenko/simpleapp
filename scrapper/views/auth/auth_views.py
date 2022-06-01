from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView, FormView, TemplateView, UpdateView

from scrapper.auth import decode_token
from scrapper.models.user import User

from .auth_forms import (
    ActivationForm,
    ChangePasswordForm,
    RegisterForm,
    ResetPasswordConfirmForm,
    ResetPasswordForm,
)


class LoginView(LoginRequiredMixin, TemplateView):
    template_name = "scrapper/auth/login.html"


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = "scrapper/auth/register.html"
    success_url = reverse_lazy("activation")

    def form_valid(self, form):
        form.cleaned_data["email"] = form.data["username"]
        form.cleaned_data["password"] = form.data["password"]
        form.cleaned_data["password2"] = form.data["password2"]
        form.save()
        return super().form_valid(form)


class ActivationView(FormView):
    form_class = ActivationForm
    template_name = "scrapper/auth/confirm.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.cleaned_data["email"] = form.data["username"]
        form.cleaned_data["code"] = form.data["code"]
        form.save()
        return super().form_valid(form)


class ResetPassowrd(FormView):
    form_class = ResetPasswordForm
    template_name = "scrapper/auth/reset_password.html"
    success_url = reverse_lazy("success")

    def form_valid(self, form):
        form.cleaned_data["email"] = form.data["username"]
        form.save()
        return super().form_valid(form)


class AccountDelete(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "scrapper/auth/delete.html"
    success_url = reverse_lazy("dashboard")


class PasswordUpdate(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ChangePasswordForm
    template_name = "scrapper/auth/change_password.html"
    success_url = reverse_lazy("private_dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_id"] = self.request.user.id
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ResetPassowrdConfirm(FormView):
    form_class = ResetPasswordConfirmForm
    template_name = "scrapper/auth/reset_password_confirm.html"
    success_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        token = self.request.resolver_match.kwargs.get("token")
        is_unvalid = False
        try:
            decode_token(token)
        except:
            is_unvalid = True
        context["token"] = token
        context["is_unvalid"] = is_unvalid
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
