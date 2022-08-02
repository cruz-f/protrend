from django import forms
from django.contrib.auth import get_user_model, authenticate, password_validation
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm, \
    UsernameField
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class SignInForm(AuthenticationForm):
    username = UsernameField(disabled=True, required=False)
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(
            attrs={'autocomplete': 'email',
                   'type': 'email',
                   'name': 'email',
                   "placeholder": "Email",
                   "class": "form-control"}
        )
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'current-password',
                   'type': 'password',
                   "placeholder": "Password",
                   "class": "form-control"}
        )
    )

    error_messages = {
        'invalid_login': _("Incorrect e-mail and/or password."),
        'inactive': _("This account is inactive."),
    }

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class SignUpForm(UserCreationForm):
    error_messages = {
        'password_mismatch': _('The two password fields did not match.'),
    }
    first_name = forms.CharField(
        required=False,
        label=_("First name"),
        max_length=60,
        widget=forms.TextInput(
            attrs={'autocomplete': 'given-name',
                   'type': 'text',
                   'name': 'first_name',
                   "placeholder": "First name",
                   "class": "form-control"}
        )
    )
    last_name = forms.CharField(
        required=False,
        label=_("Last name"),
        max_length=60,
        widget=forms.TextInput(
            attrs={'autocomplete': 'family-name',
                   'type': 'text',
                   'name': 'last_name',
                   "placeholder": "Last name",
                   "class": "form-control"}
        )
    )
    username = UsernameField(
        required=True,
        widget=forms.TextInput(
            attrs={'autocapitalize': 'none',
                   'autocomplete': 'username',
                   'autofocus': False,
                   'type': 'username',
                   'name': 'username',
                   "placeholder": "Username",
                   "class": "form-control"}
        )
    )
    email = forms.EmailField(
        required=True,
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(
            attrs={'autocomplete': 'email',
                   'autofocus': False,
                   'type': 'email',
                   'name': 'email',
                   "placeholder": "Email",
                   "class": "form-control"}
        )
    )
    institution = forms.CharField(
        required=False,
        label=_("Institution"),
        max_length=90,
        widget=forms.TextInput(
            attrs={'autocomplete': 'organization-title',
                   'type': 'text',
                   'name': 'institution',
                   "placeholder": "Institution",
                   "class": "form-control"}
        )
    )
    password1 = forms.CharField(
        required=True,
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password',
                   "placeholder": "Password",
                   "class": "form-control"}
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        required=True,
        label=_("Password confirmation"),
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password',
                   "placeholder": "Password confirmation",
                   "class": "form-control"
                   }
        ),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'institution', 'password1', 'password2')


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(
            attrs={'autocomplete': 'email',
                   'autofocus': True,
                   'type': 'email',
                   'name': 'email',
                   "placeholder": "Email",
                   "class": "form-control"}
        )
    )


class UserPasswordSetForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password',
                   'placeholder': 'New password',
                   "class": "form-control"}
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password',
                   'placeholder': 'New password confirmation',
                   "class": "form-control"}
        ),
    )


class SearchForm(forms.Form):
    search = forms.CharField(
        label=_("Search"),
        max_length=150,
        widget=forms.TextInput(
            attrs={'autocomplete': 'off',
                   'type': 'search',
                   'name': 'search',
                   "placeholder": "Search for organisms, genes, regulators, etc.",
                   "class": "form-control"}
        )
    )
