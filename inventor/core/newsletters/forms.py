from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Div
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class NewsletterForm(forms.Form):
    email = forms.EmailField(label=_('Enter your e-mail'), required=True)

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['placeholder'] = self.fields[field_name].label
            self.fields[field_name].label = ''

        self.helper = FormHelper()
        self.helper.form_action = reverse('inventor:newsletter')
        self.helper.form_class = 'form-inline justify-content-md-end justify-content-center'
        self.helper.layout = Layout(
            Row(
                Div('email', css_class='col-sm'),
                Div(Submit('submit', _('Subscribe'), css_class='btn-primary'), css_class='col-sm-auto d-flex justify-content-center')
            )
        )

        self.cookies_accepted = request.COOKIES.get('isCookieAccepted', 'no') == 'yes'

        # TODO: when cookies accepted and form submitted on the same request, we need to skip captcha

        if not settings.DEBUG and self.cookies_accepted:
            # add captcha field dynamically because we have multiple forms on a single page
            self.fields['captcha'] = ReCaptchaField(label='', widget=ReCaptchaV3())
            self.helper.layout.append('captcha')

    def clean(self):
        if not self.cookies_accepted:
            raise ValidationError(_('Please accept cookies at first to verify you are not a robot'))

        return super().clean()
