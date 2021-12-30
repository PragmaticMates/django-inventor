import django_filters
from crispy_forms.layout import Layout
from django import forms
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.forms import HiddenInput
from django.utils.translation import ugettext_lazy as _
from django_select2.forms import ModelSelect2Widget
from mptt.forms import TreeNodeMultipleChoiceField, TreeNodeChoiceField

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
        to_field_name='slug',
        widget=ModelSelect2Widget(
            model=Locality,
            queryset=Locality.objects.all(),
            search_fields=['title__icontains'],
            data_view='auto-slug-json',
            attrs={'data-minimum-input-length': 0}
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

    def __init__(self, listing_type=None, lexicon=None, inheritance=False, *args, **kwargs):
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

        # categories, localities and features searched by slug
        # self.filters['categories'].field_name = 'categories__slug_i18n'
        self.filters['categories'].method = 'filter_categories'  # search by nested categories as well
        self.filters['features'].field_name = 'features__slug_i18n'
        self.filters['features'].conjoined = True  # changed filter logic of features

        # by default, show all parent categories in the filter:
        # self.form.fields['categories'].queryset = Category.objects.filter(parent=None)
        # self.form.fields['categories'].queryset = Category.objects.all()  # use this with TreeNodeMultipleChoiceField only

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
                field_prefix = f'{listing_type.__name__.lower()}__' if inheritance else ''

                self.filters['duration'] = SliderFilter(
                    label=_('Duration'), min_value=5, max_value=60, step=5, appended_text='min',
                    has_range=True, show_inputs=False, queryset_method='published', segment=segment, field_name=f'{field_prefix}duration'
                )
                self.filters['duration'].init_segments(segment)
                self.form.fields['duration'] = self.filters['duration'].field
            except FieldDoesNotExist:
                pass  # do not add duration if it does not exist
        else:
            self.form.fields['categories'].queryset = Category.objects.all()  # use this with TreeNodeMultipleChoiceField only

        if not self.form.fields['categories'].queryset.exists():
            self.form.fields['categories'].widget = HiddenInput()
        else:
            # self.form.fields['categories'] = forms.MultipleChoiceField(
            #     label=_('Categories'),
            #     choices=list(self.form.fields['categories'].queryset.values_list('slug_i18n', 'title_i18n')),  # TODO: cache?
            #     required=False,
            #     widget=forms.CheckboxSelectMultiple
            # )

            categories_widget = self.get_widget_by_settings('categories')
            categories_field = TreeNodeMultipleChoiceField if categories_widget == forms.CheckboxSelectMultiple else TreeNodeChoiceField
            self.form.fields['categories'] = categories_field(
                label=_('Categories'),
                queryset=self.form.fields['categories'].queryset,
                to_field_name='slug_i18n',
                required=False,
                widget=categories_widget,
                level_indicator=''
            )

        if not self.form.fields['features'].queryset.exists():
            self.form.fields['features'].widget = HiddenInput()
        else:
            self.form.fields['features'] = forms.MultipleChoiceField(
                label=_('Features'),
                choices=list(self.form.fields['features'].queryset.values_list('slug_i18n', 'title')),  # TODO: cache?
                required=False,
                widget=forms.CheckboxSelectMultiple
            )

        self.hide_fields_by_settings(listing_type, lexicon)

    def get_widget_by_settings(self, field):
        widgets = settings.LISTING_FILTER.get('widgets', {})

        # currently supported for categories only
        if field != 'categories':
            raise NotImplementedError("Other then 'categories' field not supported")

        return getattr(forms, widgets.get(field, 'CheckboxSelectMultiple'))

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

    def filter_categories(self, queryset, name, value):
        if not value:
            return queryset

        if isinstance(value, Category):
            return queryset.of_category(value)

        return queryset.of_categories(value, deep=True)
