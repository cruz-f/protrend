from django.views.defaults import page_not_found, server_error, permission_denied, bad_request


# special case, as the template is not in the same sub-app as the view
def error_400(request, exception=None):
    return bad_request(request, exception, template_name='website/400.html')


# special case, as the template is not in the same sub-app as the view
def error_403(request, exception=None):
    return permission_denied(request, exception, template_name='website/403.html')


# special case, as the template is not in the same sub-app as the view
def error_404(request, exception=None):
    return page_not_found(request, exception, template_name='website/404.html')


# special case, as the template is not in the same sub-app as the view
def error_500(request):
    return server_error(request, template_name='website/500.html')
