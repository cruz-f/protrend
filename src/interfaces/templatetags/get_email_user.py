from django.template.defaulttags import register


@register.filter
def get_email_user(email):
    if hasattr(email, 'split'):
        return email.split('@')[0]

    return
