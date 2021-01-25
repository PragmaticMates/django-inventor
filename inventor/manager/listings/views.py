from django.core.validators import EMPTY_VALUES
from django.db.models import F
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView
from inventor.core.bookings.models import Booking
from pragmatic.mixins import DisplayListViewMixin, SortingListViewMixin

from inventor.core.lexicons.models import Category
from inventor.core.listings.filters import ListingFilter
from inventor.core.listings.models.general import Listing


class ListingListView(DisplayListViewMixin, SortingListViewMixin, ListView):
    model = Listing
    template_name = 'manager/listings/listing_list.html'
    filter_class = ListingFilter
    paginate_by = 12
    displays = ['rows']
    paginate_by_display = {'rows': [12, 24, 48]}
    sorting_options = {
        '-created': _('Newest'),
        'created': _('Oldest'),
        # '-modified': _('Recently modified'),
        'price': _('Price (Low to high)'),
        '-price': _('Price (High to low)'),
        'title': _('Title'),
    }

    def get_sorting_options(self):
        return {**{'-promoted': (_('Promoted'), ['-promoted', 'awaiting', 'created'])}, **self.sorting_options}

    def dispatch(self, request, *args, **kwargs):
        # redirect to category detail view if single category requested
        requested_categories = request.GET.getlist('categories')
        if len(requested_categories) == 1:
            category = Category.objects.get(slug_i18n=requested_categories[0])
            params = request.GET.copy()
            del params['categories']
            params = f'?{params.urlencode()}' if params not in EMPTY_VALUES else ''
            url = f"{category.get_absolute_url()}{params}"
            return redirect(url)

        self.filter = self.filter_class(**self.get_filter_kwargs())
        return super().dispatch(request, *args, **kwargs)

    def get_filter_kwargs(self):
        return {
            'data': self.request.GET,
            'queryset': self.get_whole_queryset(),
            'listing_type': None if self.model == Listing else self.model,
        }

    def get_template_names(self):
        names = super().get_template_names()
        names.insert(1, f"manager/listings/listing{self.template_name_suffix}.html")
        return names

    def get_queryset(self):
        queryset = self.filter.qs\
            .annotate(locality_title=F('locality__title'))\
            .prefetch_related('categories')
        return self.sort_queryset(queryset)

    def get_whole_queryset(self):
        qs = super().get_queryset()\
            .published()\
            .not_hidden()\
            .order_by('-promoted', 'modified')

        if self.model == Listing:
            qs = qs.select_subclasses()

        return qs

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({
            'title': self.model._meta.verbose_name_plural,
            'filter': self.filter
        })
        return context_data


class ListingStatsView(DetailView):
    model = Listing
    template_name = 'manager/listings/listing_stats.html'
    slug_field = 'slug_i18n'

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

    # def get_queryset(self):
    #     return super().get_queryset().published().only('id')  # TODO: not published listings are visible for staff and listing author

    def get_object(self, queryset=None):
        return super().get_object(queryset).get_real_instance()

    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #
    #     context_data.update({
    #         'all_features': Feature.objects.all(),
    #         'features': self.object.features.all(),
    #     })
    #
    #     try:
    #         # TODO: refactor
    #         from inventor.core.lexicons.models import AccommodationAmenity
    #         from inventor.core.listings.models.listing_types import Accommodation
    #         if isinstance(self.object, Accommodation):
    #             context_data.update({
    #                 'all_amenities': AccommodationAmenity.objects.all(),
    #                 'amenities': self.object.amenities.all(),
    #             })
    #     except ImportError:
    #         pass
    #
    #     return context_data

    def get_template_names(self):
        names = super().get_template_names()
        obj = self.get_object()
        return [f"manager/listings/{obj.__class__.__name__.lower()}_stats.html"] + names


class ListingBookingsListView(DisplayListViewMixin, SortingListViewMixin, ListView):
    model = Booking
    template_name = 'manager/listings/listing_bookings_list.html'
    # filter_class = BookingFilter
    paginate_by = 12
    displays = ['rows']
    paginate_by_display = {'rows': [12, 24, 48]}
    sorting_options = {
        '-created': _('Newest'),
        'created': _('Oldest'),
    }
    slug_field = 'slug'

    def dispatch(self, request, *args, **kwargs):
        self.listing_slug = self.kwargs.get(self.slug_field)
        self.listing = Listing.objects.get(slug=self.listing_slug)
        print(self.listing_slug)
        # self.filter = self.filter_class(**self.get_filter_kwargs())
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(listing__slug=self.listing_slug)

    def get_template_names(self):
        names = super().get_template_names()
        names.insert(1, f"manager/listings/listing_bookings{self.template_name_suffix}.html")
        return names

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({
            'object': self.listing
        })
        return context_data
