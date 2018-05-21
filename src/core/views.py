# coding: utf-8

from django.shortcuts import render
from django.conf import settings
from django.views import csrf
from django.views import defaults
from django.views.csrf import CSRF_FAILURE_TEMPLATE_NAME


def csrf_failure(request, reason="", template_name=CSRF_FAILURE_TEMPLATE_NAME, force_display=False):
    if not settings.DEBUG or force_display:
        return render(request, 'errors/403_csrf.html', {})

    return csrf.csrf_failure(request, reason=reason)


def page_not_found(*args, **kwargs):
    kwargs['template_name'] = 'errors/404.html'
    return defaults.page_not_found(*args, **kwargs)


def server_error(*args, **kwargs):
    kwargs['template_name'] = 'errors/500.html'
    return defaults.server_error(*args, **kwargs)


def bad_request(*args, **kwargs):
    kwargs['template_name'] = 'errors/400.html'
    return defaults.bad_request(*args, **kwargs)


def permission_denied(*args, **kwargs):
    kwargs['template_name'] = 'errors/403.html'
    return defaults.permission_denied(*args, **kwargs)
