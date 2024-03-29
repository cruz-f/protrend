from django.contrib.auth import views as auth_views, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from interfaces.website.forms import SignInForm, SignUpForm, UserPasswordResetForm, UserPasswordSetForm
from interfaces.website.tokens import account_activation_token

User = get_user_model()


class SignInView(auth_views.LoginView):
    form_class = SignInForm
    template_name = 'website/sign_in.html'


class LogoutView(auth_views.LogoutView):
    template_name = 'website/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'home'
        return context


def sign_up(request):
    msg = None
    success = False

    if request.method == 'POST':

        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            current_site = get_current_site(request)
            message = render_to_string(
                template_name='website/activation_email.html',
                context={'username': user.username,
                         'protocol': 'https' if request.is_secure() else 'http',
                         'domain': current_site.domain,
                         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                         'token': account_activation_token.make_token(user)}
            )
            subject = 'ProTReND - Account Activation'
            user.email_user(subject, message)

            msg = 'Please confirm your email address to complete the registration. ' \
                  'If you do not receive our email in your inbox, please check your spam folder.'
            success = True

        else:
            msg = "Ups! There was an error while trying to sign you up. " \
                  "Please check the fields or contact the support team."
            success = False

    else:
        form = SignUpForm()

    return render(request, 'website/sign_up.html', {"form": form, "msg": msg, "success": success})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        return render(request, 'website/successful_activation.html')

    else:
        return render(request, 'website/failed_activation.html')


class PasswordResetView(auth_views.PasswordResetView):
    form_class = UserPasswordResetForm
    template_name = 'website/password_reset.html'
    email_template_name = 'website/password_reset_email.html'
    subject_template_name = 'website/password_reset_subject.txt'


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'website/password_reset_done.html'


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    form_class = UserPasswordSetForm
    template_name = 'website/password_reset_confirm.html'


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'website/password_reset_complete.html'
