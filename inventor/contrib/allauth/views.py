from allauth.account.forms import LoginForm, SignupForm
from allauth.account.views import RedirectAuthenticatedUserMixin
from allauth.utils import get_request_param
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.module_loading import import_string
from django.views.generic import TemplateView


class LoginSignUpView(RedirectAuthenticatedUserMixin, TemplateView):
    template_name = 'account/login-signup.html'
    success_url = None
    redirect_field_name = "next"
    context = None

    def get_context_data(self, **kwargs):
        ret = super().get_context_data(**kwargs)
        site = get_current_site(self.request)
        redirect_field_value = get_request_param(self.request,
                                                 self.redirect_field_name)

        ret.update({
            "site": site,
            "redirect_field_name": self.redirect_field_name,
            "redirect_field_value": redirect_field_value,
        })

        ret.update(self.get_account_forms())

        return ret

    def get_form_kwargs(self):
        kwargs = {'initial': {}}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_form_class(self, form):
        return import_string(settings.ACCOUNT_FORMS.get(form))

    def get_account_forms(self):
        form_kwargs = self.get_form_kwargs()

        return {
            'login_form': self.get_form_class('login')(**form_kwargs),
            'signup_form': self.get_form_class('signup')(**form_kwargs),
        }

    def get_success_url(self):
        return settings.LOGIN_REDIRECT_URL
