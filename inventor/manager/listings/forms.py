from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import Layout, Row, Div, Submit
from django import forms
from django.utils.translation import ugettext_lazy as _
from pragmatic.forms import SingleSubmitFormHelper

from inventor.core.listings.models.general import Listing


class ListingInfoForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title_i18n', 'slug_i18n', 'description_i18n']
        widgets = {
            'description_i18n': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description_i18n'].required = True
        self.helper = SingleSubmitFormHelper()
        self.helper.layout = Layout(
            Row(
                Div('title_i18n', css_class='col-sm-6'),
                Div('slug_i18n', css_class='col-sm-6'),
                Div('description_i18n', css_class='col-12'),
            ),
            FormActions(
                Submit('submit', _('Submit'), css_class='btn-secondary')
            )
        )