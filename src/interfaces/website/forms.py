from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User


class SignInForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                'type': 'email',
                'name': 'email',
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'type': 'password',
                "placeholder": "Password",
                "class": "form-control"
            }
        ))

    error_messages = {
        'invalid_login': "Incorrect e-mail and/or password.",
        'inactive': "This account is inactive.",
    }


class SignUpForm(UserCreationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'type': 'email',
                'name': 'email',
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        'placeholder': 'Enter your email',
        'type': 'email',
        'name': 'email'}))


class UserPasswordSetForm(SetPasswordForm):
    error_messages = {
        'password_mismatch': 'Password confirmation failed. Please enter the same password as before.',
    }
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                          'placeholder': 'New password',
                                          "class": "form-control"}),
        strip=False,
    )
    new_password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                          'placeholder': 'New password confirmation',
                                          "class": "form-control"}),
    )
