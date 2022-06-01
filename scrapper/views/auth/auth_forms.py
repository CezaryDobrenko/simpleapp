import time
from random import randint

from django import forms
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.urls import reverse

from scrapper.auth import decode_token, encode_token
from scrapper.models.user import User
from scrapper.views.basic_forms import BaseForm


def check_is_password_is_strong(password):
    num_exist = False
    upper_char = False
    lower_char = False

    for p_character in password:
        if p_character.isdigit():
            num_exist = True
        if p_character.isupper():
            upper_char = True
        if p_character.islower():
            lower_char = True

    message = []
    if len(password) < 8:
        message.append("Hasło musi mieć przynajmniej 8 znaków")
    if not num_exist:
        message.append("Hasło musi zawierać cyfrę")
    if not upper_char:
        message.append("Hasło musi zawierać przynajmniej jedną dużą literę")
    if not lower_char:
        message.append("Hasło musi zawierać przynajmniej jedną małą literę")

    return message


class RegisterForm(BaseForm):
    class Meta:
        model = User
        fields = []

    def clean(self):
        errors = []
        is_email_exist = User.objects.filter(email=self.data["username"]).count()
        if self.data["password"] != self.data["password2"]:
            errors.append("Podano różne hasła")
        if is_email_exist > 0:
            errors.append("Podany email już istnieje w systemie")
        if messages := check_is_password_is_strong(self.data["password"]):
            errors = errors + messages
        if errors:
            raise forms.ValidationError(errors)

    def save(self, commit=True):
        random_pin = randint(100000, 999999)
        user = User(
            username=self.data["username"],
            email=self.data["username"],
            verification_pin=random_pin,
            is_active=False,
        )
        user.set_password(self.data["password"])
        user.save()
        email = EmailMessage(
            "Aktywacja konta w platformie SCRAPPERHUB",
            f"Kod aktywacyjny: {random_pin}",
            to=[self.data["username"]],
        )
        email.send()


class ResetPasswordConfirmForm(BaseForm):
    class Meta:
        model = User
        fields = []

    def clean(self):
        errors = []
        if self.data["new_password"] != self.data["confirm_password"]:
            errors.append("Podano różne hasła")
        if messages := check_is_password_is_strong(self.data["new_password"]):
            errors = errors + messages
        if errors:
            raise forms.ValidationError(errors)

    def save(self, commit=True):
        token = self.data["token"]
        payload = decode_token(token)
        user = User.objects.get(email=payload.get("email"))
        user.set_password(self.data["new_password"])
        user.save()


class ResetPasswordForm(BaseForm):
    class Meta:
        model = User
        fields = []

    def clean(self):
        errors = []
        user = User.objects.filter(email=self.data["username"]).first()
        if user is None:
            errors.append("Podany email nie istnieje w systemie")
        if errors:
            raise forms.ValidationError(errors)

    def save(self, commit=True):
        payload = {"email": self.data["username"], "exp": time.time() + 3600}
        token = encode_token(payload)
        link = f"http://localhost/reset_password_confirm/{token}"
        email = EmailMessage(
            "Reset hasła do konta w platformie SCRAPPERHUB",
            f"Link pozwalający na reset hasła: {link}",
            to=[self.data["username"]],
        )
        email.send()


class ChangePasswordForm(BaseForm):
    class Meta:
        model = User
        fields = []

    def clean(self):
        errors = []
        user = User.objects.get(id=self.data["user_id"])
        if not user.check_password(self.data["old_password"]):
            errors.append("Nieprawidłowe aktualne hasło")
        if self.data["new_password"] != self.data["new_password_confirm"]:
            errors.append("Podane nowe hasło nie zgadza się z polem potwierdź hasło")
        if messages := check_is_password_is_strong(self.data["new_password"]):
            errors = errors + messages
        if errors:
            raise forms.ValidationError(errors)

    def save(self, commit=True):
        user = User.objects.get(id=self.data["user_id"])
        user.set_password(self.data["new_password"])
        user.save()
        return HttpResponseRedirect(reverse("private_dashboard"))


class ActivationForm(BaseForm):
    class Meta:
        model = User
        fields = []

    def clean(self):
        errors = []
        user = User.objects.filter(email=self.data["username"]).first()
        if user is None:
            errors.append("Podany email nie istnieje w systemie")
        elif user.is_active is True:
            errors.append("Konto zostało już aktywowane")
        else:
            if user.verification_pin != self.data["code"]:
                errors.append("Podano nieprawidowy kod")
        if errors:
            raise forms.ValidationError(errors)

    def save(self, commit=True):
        user = User.objects.filter(email=self.data["username"]).first()
        user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse("login"))
