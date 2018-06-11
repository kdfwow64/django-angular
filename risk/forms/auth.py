"""Forms for auth module."""
from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import PasswordInput
from django.core.validators import validate_email
from ..models.auth import User


def unique_email(value):
    """Email validator."""
    if User.objects.filter(email=value).first():
        raise ValidationError('Email is already in use.')


class LoginForm(forms.Form):
    """Login Form."""

    email = forms.EmailField(
        label='Email', required=True, validators=[validate_email])
    password = forms.CharField(
        label='Password', required=True, widget=PasswordInput)


class RegistrationForm(forms.Form):
    """Form for users to create new account."""

    email = forms.EmailField(label='Email', required=True, validators=[
                             validate_email, unique_email])
    full_name = forms.CharField(label='Full Name', required=True)
    password = forms.CharField(
        label='Password', required=True, widget=PasswordInput)
    confirm_password = forms.CharField(
        label='Confirm Password', required=True, widget=PasswordInput)

    def clean(self):
        """Clean data."""
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        if confirm_password != password:
            self.add_error(
                "password", "Password and confirm password should match!")
