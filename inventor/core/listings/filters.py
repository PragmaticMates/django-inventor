import django_filters
from crispy_forms.layout import Layout
from django import forms
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.forms import HiddenInput
from django.utils.translation import ugettext_lazy as _
from django_select2.forms import ModelSelect2Widget

from inventor import settings
from pragmatic.filters import SliderFilter

from inventor.core.lexicons.models import Category, Locality
from inventor.core.listings.models.general import Listing
from inventor.utils import SingleSubmitFormHelper, PositiveBooleanFilter


class ListingFilter(django_filters.FilterSet):
    keyword = django_filters.CharFilter(label=_('Keyword'), method=lambda qs, name, value: qs.by_keyword(value))
    price = SliderFilter(label=_('Price'), min_value=0, max_value=1000, step=10, appended_text=' €', has_range=True, show_inputs=False, queryset_method='published', segment='listings.Listing.price')
    locality = django_filters.ModelChoiceFilter(
        label=_('Locality'),
        queryset=Locality.objects.all(),
        widget=ModelSelect2Widget(
            model=Locality,
            queryset=Locality.objects.all(),
            search_fields=['title__icontains'],
        )
    )

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

    def __init__(self, listing_type=None, lexicon=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = SingleSubmitFormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            'keyword',
            'promoted',
            'locality',
            'price',
            'duration',
            'categories', 'features'
        )
        self.form.fields['locality'].empty_label = _('All localities')

        if not Listing.objects.published().promoted().exists():
            self.form.fields['promoted'].widget = HiddenInput()

        if not self.form.fields['locality'].queryset.exists():
            self.form.fields['locality'].widget = HiddenInput()

        # categories and localities searched by slug
        self.filters['categories'].field_name = 'categories__slug_i18n'

        if listing_type:
            # dynamic categories
            listing_type_categories = Category.objects.of_listing_type(listing_type)

            if listing_type_categories.exists():
                self.form.fields['categories'].queryset = listing_type_categories

            if listing_type_categories.exclude(parent=None).exists():
                self.form.fields['categories'].queryset = listing_type_categories.exclude(parent=None)

            # dynamic price segment based on listing type
            segment = f'listings.{listing_type.__name__}.price'
            self.filters['price'].init_segments(segment)
            self.form.fields['price'] = self.filters['price'].field

            # hide price if not required
            if not Listing.objects.published().with_price().exists():
                self.form.fields['price'].widget = HiddenInput()

            # Exercise duration
            try:
                listing_type._meta.get_field('duration')
                self._meta.fields.append('duration')
                segment = f'listings.{listing_type.__name__}.duration'
                self.filters['duration'] = SliderFilter(
                    label=_('Duration'), min_value=5, max_value=60, step=5, appended_text='min',
                    has_range=True, show_inputs=False, queryset_method='published', segment=segment, field_name='duration'
                )
                self.filters['duration'].init_segments(segment)
                self.form.fields['duration'] = self.filters['duration'].field
            except FieldDoesNotExist:
                pass  # do not add duration if it does not exist

        else:
            self.form.fields['categories'].queryset = Category.objects.filter(parent=None)

        if not self.form.fields['categories'].queryset.exists():
            self.form.fields['categories'].widget = HiddenInput()
        else:
            self.form.fields['categories'] = forms.MultipleChoiceField(
                label=_('Categories'),
                choices=list(self.form.fields['categories'].queryset.values_list('slug_i18n', 'title_i18n')),  # TODO: cache?
                required=False,
                widget=forms.CheckboxSelectMultiple
            )

        if not self.form.fields['features'].queryset.exists():
            self.form.fields['features'].widget = HiddenInput()
        else:
            self.form.fields['features'] = forms.MultipleChoiceField(
                label=_('Features'),
                choices=list(self.form.fields['features'].queryset.values_list('pk', 'title')),  # TODO: cache?
                required=False,
                widget=forms.CheckboxSelectMultiple
            )

            # changed filter logic of features
            self.filters['features'].method = 'filter_features'

        self.hide_fields_by_settings(listing_type, lexicon)

    def hide_fields_by_settings(self, listing_type, lexicon):
        hidden_fields = settings.LISTING_FILTER.get('hidden_fields', {})

        for field_name, subjects in hidden_fields.items():
            if field_name not in self.form.fields:
                continue

            subjects = subjects or {}

            listing_types = subjects.get('listing_types')
            lexicons = subjects.get('lexicons')

            if listing_types is None or \
                (listing_type and listing_type.__name__ in listing_types):
                del self.form.fields[field_name]
                # self.form.fields[field_name].widget = HiddenInput()
                continue

            if lexicons is None or \
                (lexicon and lexicon.__name__ in lexicons):
                del self.form.fields[field_name]
                # self.form.fields[field_name].widget = HiddenInput()
                continue

    def filter_features(self, queryset, name, value):
        # return listings having ALL features, not AT LEAST one
        for feature in value:
            queryset = queryset.filter(features=feature)
        return queryset
