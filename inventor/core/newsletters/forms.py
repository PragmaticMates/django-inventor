from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from django.conf import settings
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class NewsletterForm(forms.Form):
    email = forms.EmailField(label=_('Enter your e-mail'), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            self.fields[field_name].widget.attrs['placeholder'] = self.fields[field_name].label
            self.fields[field_name].label = ''

        self.helper = FormHelper()
        self.helper.form_action = reverse('inventor:newsletter')
        self.helper.form_class = 'form-inline justify-content-end'
        self.helper.layout = Layout(
            'email',
            Submit('submit', _('Subscribe'), css_class='ml-3 btn-primary'),
        )

        if not settings.DEBUG:
            # add captcha field dynamically because we have multiple forms on a single page
            self.fields['captcha'] = ReCaptchaField(label='', widget=ReCaptchaV3())
            self.helper.layout.append('captcha')
