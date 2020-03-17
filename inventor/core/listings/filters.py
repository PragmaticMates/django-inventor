import django_filters
from crispy_forms.bootstrap import InlineRadios
from crispy_forms.layout import Layout
from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _

from inventor.core.lexicons.models import Category
from inventor.core.listings.models.general import Listing
from inventor.utils import SingleSubmitFormHelper, PositiveBooleanFilter
from pragmatic.filters import SliderFilter


class ListingFilter(django_filters.FilterSet):
    keyword = django_filters.CharFilter(label=_('Keyword'), method=lambda qs, name, value: qs.by_keyword(value))
    price = SliderFilter(label=_('Price'), min_value=0, max_value=1000, step=10, appended_text=' €', has_range=True, segment='listings.Listing.price')

    class Meta:
        model = Listing
        fields = [
            'keyword',
            'promoted',
            'locality',
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

    def __init__(self, listing_type=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = SingleSubmitFormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            'keyword',
            'promoted',
            'locality',
            'price',
            'categories', 'features'
        )
        self.form.fields['locality'].empty_label = _('All localities')

        # categories searched by slug
        self.filters['categories'].field_name = 'categories__slug'

        if listing_type:
            # dynamic categories
            self.form.fields['categories'].queryset = Category.objects.of_listing_type(listing_type).exclude(parent=None)

            # dynamic segment based on listing type
            segment = f'listings.{listing_type.__name__}.price'
            self.filters['price'].init_segments(segment)
            self.form.fields['price'] = self.filters['price'].field
            # self.filters['price'] = SliderFilter(label=_('Price'), min_value=0, max_value=1000, step=10, appended_text=' €', has_range=True, segment=segment)
            # self.price = SliderFilter(label=_('Price'), min_value=0, max_value=1000, step=10, appended_text=' €', has_range=True, segment=segment)

        else:
            self.form.fields['categories'].queryset = Category.objects.filter(parent=None)

        self.form.fields['categories'] = forms.MultipleChoiceField(
            label=_('Categories'),
            choices=list(self.form.fields['categories'].queryset.values_list('slug', 'title')),  # TODO: cache?
            required=False,
            widget=forms.CheckboxSelectMultiple
        )

        # changed filter logic of features
        self.filters['features'].method = 'filter_features'

    def filter_features(self, queryset, name, value):
        # return listings having ALL features, not AT LEAST one
        for feature in value:
            queryset = queryset.filter(features=feature)
        return queryset
