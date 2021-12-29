from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Fieldset, Row
from django import forms
from django.forms import Textarea
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from inventor.core.bookings.models import Booking


class BookingForm(forms.ModelForm):
    book_from = forms.DateField(label=_('Check-in'), required=True)  # TODO: DateTime for tickets, restaurant table, ...
    book_to = forms.DateField(label=_('Check-out'), required=True)
    number_of_persons = forms.IntegerField(label=_('Persons'), required=True, min_value=1)
    person = forms.CharField(label='', required=True)
    email = forms.EmailField(label='', required=True)
    phone = forms.CharField(label='', required=True)
    message = forms.CharField(label='', required=False, widget=Textarea(attrs={'rows': 4}))
    agree_processing = forms.BooleanField(label=_('I agree to the processing of my personal data'), required=True)

    class Meta:
        model = Booking
        fields = [
            'book_from', 'book_to',
            'number_of_persons',
            'person', 'email', 'phone',
            'message'
        ]

    def __init__(self, listing, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.listing = listing

        self.fields['book_from'].widget.attrs['placeholder'] = 'dd.mm.yyyy'
        self.fields['book_to'].widget.attrs['placeholder'] = 'dd.mm.yyyy'
        self.fields['number_of_persons'].widget.attrs['placeholder'] = _('Number of guests')
        self.fields['person'].widget.attrs['placeholder'] = _('Contact person')
        self.fields['email'].widget.attrs['placeholder'] = _('E-mail')
        self.fields['phone'].widget.attrs['placeholder'] = _('Phone')
        self.fields['message'].widget.attrs['placeholder'] = _('Send a question or inquiry directly to the accommodation owner without increasing the price')

        self.helper = FormHelper()
        self.helper.form_action = reverse('inventor:bookings:book_listing', args=(listing.slug_i18n,))
        self.helper.form_class = 'booking-form'
        self.helper.layout = Layout(
            Row(
                Div(Div('book_from', css_class='datetime-picker'), css_class='col-md-6'),
                Div(Div('book_to', css_class='datetime-picker'), css_class='col-md-6'),
            ),
            'number_of_persons',
            Fieldset(
                _('Contact information'),
                'person',
                'email',
                'phone',
                'message',
            ),
            'agree_processing',
            FormActions(
                Submit('submit', _('Send request'), css_class='w-100'), css_class='mb-0'
            )
        )

    def save(self, commit=True):
        booking = super().save(commit=False)
        booking.listing = self.listing
        booking.save()
        return booking
