from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Fieldset
from django import forms
from django.forms import Textarea
from django.utils.translation import ugettext_lazy as _


class BookingForm(forms.Form):
    # todo decide what is required
    check_in = forms.DateField(label=_('Check-in'), required=True)
    check_out = forms.DateField(label=_('Check-out'), required=True)
    persons = forms.IntegerField(label=_('Persons'), required=True, min_value=1)
    name = forms.CharField(label='', required=True)
    email = forms.EmailField(label='', required=True)
    phone = forms.CharField(label='', required=True)
    message = forms.CharField(label='', required=True, widget=Textarea(attrs={'rows': 4}))
    agree_processing = forms.BooleanField(label=_('I agree to the processing of my personal data'), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['check_in'].widget.attrs['placeholder'] = 'dd.mm.yyyy'
        self.fields['check_out'].widget.attrs['placeholder'] = 'dd.mm.yyyy'
        self.fields['persons'].widget.attrs['placeholder'] = _('Number of guests')

        self.fields['name'].widget.attrs['placeholder'] = _('Contact person')
        self.fields['email'].widget.attrs['placeholder'] = _('E-mail')
        self.fields['phone'].widget.attrs['placeholder'] = _('Phone')
        self.fields['message'].widget.attrs['placeholder'] = _('Send a question or inquiry directly to the accommodation owner without increasing the price')

        self.helper = FormHelper()
        self.helper.form_class = 'booking-form'
        self.helper.layout = Layout(
            Div('check_in', css_class='datetime-picker'),
            Div('check_out', css_class='datetime-picker'),
            'persons',
            Fieldset(
                _('Contact information'),
                'name',
                'email',
                'phone',
                'message',
            ),
            'agree_processing',
            FormActions(
                Submit('submit', _('Send request'), css_class='w-100')
            )
        )
