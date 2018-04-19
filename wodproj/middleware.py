import re
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse

EXEMPT_URLS =[re.compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]

PRO_URLS =[re.compile(settings.PROFESSIONAL_REDIRECT_URL.lstrip('/'))]
if hasattr(settings, 'PROFESSIONAL_URLS'):
    PRO_URLS += [re.compile(url) for url in settings.PROFESSIONAL_URLS]

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')
        #this checks the request pram has an attribute 'user'

        path = request.path_info.lstrip('/')
        person = request.user.is_authenticated


        if path == reverse('starthere:logout').lstrip('/'):
            logout(request)
        #need to define exceptions
        url_is_exempt = any(url.match(path) for url in EXEMPT_URLS)

        if person and url_is_exempt:
            return redirect(settings.LOGIN_REDIRECT_URL)

        elif person or url_is_exempt:
            return None

        else:
            return redirect(settings.LOGIN_URL)

class ProfessionalRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')

        path = request.path_info.lstrip('/')
        person = request.user.is_authenticated

        url_match = any(url.match(path) for url in PRO_URLS)

        professional = False
        if hasattr(request.user, 'professional') and person:
            professional = True

        if not professional and url_match:
            return redirect(settings.LOGIN_REDIRECT_URL)

        else:
            return None
