import django_filters
from crispy_forms.bootstrap import InlineRadios
from crispy_forms.layout import Layout
from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _

from inventor.core.listings.models.general import Listing
from inventor.utils import SingleSubmitFormHelper, PositiveBooleanFilter


class ListingFilter(django_filters.FilterSet):
    keyword = django_filters.CharFilter(label=_('Keyword'), method=lambda qs, name, value: qs.by_keyword(value))

    class Meta:
        model = Listing
        fields = [
            'keyword',
            'promoted',
            'location',
            'price',
            'categories', 'features'
        ]
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.TextField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.BooleanField: {
                'filter_class': PositiveBooleanFilter,
                'extra': lambda f: {
                    'widget': forms.CheckboxInput,
                },
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = SingleSubmitFormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            'keyword',
            'promoted',
            'location',
            'price',
            'categories', 'features'
        )
        self.form.fields['location'].empty_label = _('All locations')
