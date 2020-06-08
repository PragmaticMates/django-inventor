from django.db.models import F
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, FormView
from django.views.generic.detail import SingleObjectMixin
from pragmatic.mixins import DisplayListViewMixin, SortingListViewMixin

from inventor.core.lexicons.models import Feature, AccommodationAmenity
from inventor.core.listings.filters import ListingFilter
from inventor.core.listings.forms import BookingForm
from inventor.core.listings.models.general import Listing
from inventor.core.listings.models.listing_types import Accommodation


class ListingListView(DisplayListViewMixin, SortingListViewMixin, ListView):
    model = Listing
    filter_class = ListingFilter
    paginate_by = 12
    displays = ['columns']
    paginate_by_display = {'columns': [12, 24, 48]}
    sorting_options = {
        '-created': _('Newest'),
        'created': _('Oldest'),
        # '-modified': _('Recently modified'),
        'price': _('Price (Low to high)'),
        '-price': _('Price (High to low)'),
        'title': _('Title'),
    }

    def get_sorting_options(self):
        return {**{'-promoted': (_('Promoted'), ['-promoted', 'created'])}, **self.sorting_options}

    def dispatch(self, request, *args, **kwargs):
        self.filter = self.filter_class(data=request.GET, queryset=self.get_whole_queryset(), listing_type=None if self.model == Listing else self.model)
        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):
        names = super().get_template_names()
        names.append(f"listings/listing{self.template_name_suffix}.html")
        return names

    def get_queryset(self):
        queryset = self.filter.qs.only('id', 'slug', 'title', 'locality_id', 'locality__title', 'image', 'price', 'price_unit', 'price_starts_at', 'promoted').annotate(locality_title=F('locality__title'))
        return self.sort_queryset(queryset)

    def get_whole_queryset(self):
        return super().get_queryset().published().select_subclasses().order_by('-promoted', 'modified')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({
            'title': self.model._meta.verbose_name_plural,
            'filter': self.filter
        })
        return context_data


class ListingDetailView(SingleObjectMixin, FormView):
    model = Listing
    template_name = 'listings/listing_detail.html'
    form_class = BookingForm

    # def get_queryset(self):
    #     return super().get_queryset().select_subclasses()

    # """A base view for displaying a single object."""
    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     context = self.get_context_data(object=self.object)
    #     return self.render_to_response(context)

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().published().only('id')  # TODO: not published listings are visible for staff and listing author

    def get_object(self, queryset=None):
        return super().get_object(queryset).get_real_instance()

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data.update({
            'all_features': Feature.objects.all(),
            'features': self.object.features.all(),
        })

        if isinstance(self.object, Accommodation):
            context_data.update({
                'all_amenities': AccommodationAmenity.objects.all(),
                'amenities': self.object.amenities.all(),
            })
        return context_data

    def form_valid(self, form):
        # todo send message and inform user
        return super().form_valid(form)

    def form_invalid(self, form):
        # todo inform user
        return super().form_invalid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()
