from allauth.account.forms import LoginForm, SignupForm
from allauth.utils import get_request_param
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic import TemplateView


class LoginSignUpView(TemplateView):
    form_class_login = LoginForm
    form_class_signup = SignupForm
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

    def get_account_forms(self):
        form_kwargs = self.get_form_kwargs()

        return {
            'login_form': self.form_class_login(**form_kwargs),
            'signup_form': self.form_class_signup(**form_kwargs),
        }
