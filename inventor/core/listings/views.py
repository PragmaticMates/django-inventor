from django.apps import apps
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.validators import EMPTY_VALUES
from django.db.models import F, Count
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView
from django.views.generic.detail import BaseDetailView
from hitcount.views import HitCountDetailView

from pragmatic.mixins import DisplayListViewMixin, SortingListViewMixin
from inventor.core.lexicons.models import Feature, Category
from inventor.core.listings.filters import ListingFilter
from inventor.core.listings.models.general import Listing, Group
from inventor import settings as inventor_settings


class ListingListView(DisplayListViewMixin, SortingListViewMixin, ListView):
    model = Listing
    template_name = 'listings/listing_list.html'
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
        return {
            **{'-promoted': (_('Promoted'), inventor_settings.LISTING_SORTING_OPTIONS.get('-promoted', ['-promoted', '-rank']))},
            **self.sorting_options
        }

    def dispatch(self, request, *args, **kwargs):
        # redirect to category detail view if single category requested (not related to listing type)
        requested_categories = request.GET.getlist('categories')
        if len(requested_categories) == 1:
            category = get_object_or_404(Category, slug_i18n=requested_categories[0])
            if not category.listing_type:
                params = request.GET.copy()
                del params['categories']
                params = f'?{params.urlencode()}' if params not in EMPTY_VALUES else ''
                url = f"{category.get_absolute_url()}{params}"
                return redirect(url)

        self.filter = self.filter_class(**self.get_filter_kwargs())
        return super().dispatch(request, *args, **kwargs)

    def get_listing_class_by_queryset(self):
        subclasses = getattr(self.get_whole_queryset(), 'subclasses', None)

        if subclasses is not None and len(subclasses) == 1:
            subclass = subclasses[0]
            model = apps.get_model('listings', subclass)
            return model

        return None

    def get_filter_kwargs(self):
        listing_type = self.get_listing_class_by_queryset()

        return {
            'data': self.request.GET,
            'queryset': self.get_whole_queryset(),
            'listing_type': self.model if self.model != Listing else listing_type,
            'inheritance': False if self.model != Listing else listing_type != self.model
        }

    def get_template_names(self):
        names = super().get_template_names()
        names.append(f"listings/listing{self.template_name_suffix}.html")
        return names

    def get_queryset(self):
        queryset = self.filter.qs\
            .annotate(
                locality_title=F('locality__title'),
                favorite_of_users__count=Count('favorite_of_users')
            )\
            .prefetch_related('categories', 'groups')
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


class ListingDetailView(HitCountDetailView):
    model = Listing
    template_name = 'listings/listing_detail.html'
    slug_field = 'slug_i18n'
    count_hit = True

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

        try:
            # TODO: refactor
            from inventor.core.lexicons.models import AccommodationAmenity
            from inventor.core.listings.models.listing_types import Accommodation
            if isinstance(self.object, Accommodation):
                context_data.update({
                    'all_amenities': AccommodationAmenity.objects.all(),
                    'amenities': self.object.amenities.all(),
                })
        except ImportError:
            pass

        return context_data

    def get_template_names(self):
        names = super().get_template_names()
        obj = self.get_object()
        return [f"listings/{obj.__class__.__name__.lower()}_detail.html"] + names


class ListingSwitchFavoriteView(LoginRequiredMixin, BaseDetailView):
    model = Listing
    template_name = 'listings/listing_detail.html'
    slug_field = 'slug_i18n'

    def get(self, request, *args, **kwargs):
        listing = self.get_object()
        user = request.user

        # add or remove favorite
        if listing in user.favorite_listings.all():
            user.favorite_listings.remove(listing)
            messages.info(request, _('Listing removed from your favorite list'))
        else:
            user.favorite_listings.add(listing)
            messages.success(request, _('Listing added into your favorite list'))

        back_url = request.GET.get('back_url', listing.get_absolute_url())
        return redirect(back_url)


class ListingFavoritesView(LoginRequiredMixin, ListView):
    model = Listing
    template_name = 'listings/favorites.html'
    paginate_by = 12

    def get_queryset(self):
        return self.request.user.favorite_listings\
            .published() \
            .not_hidden() \
            .annotate(locality_title=F('locality__title')) \
            .prefetch_related('categories', 'groups') \
            .select_subclasses()


class GroupDetailView(HitCountDetailView):
    model = Group
    # template_name = 'listings/listing_detail.html'
    slug_field = 'slug_i18n'
    count_hit = True
    #
    # def get_template_names(self):
    #     names = super().get_template_names()
    #     obj = self.get_object()
    #     return [f"listings/{obj.__class__.__name__.lower()}_detail.html"] + names
