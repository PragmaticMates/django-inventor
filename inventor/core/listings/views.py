from django.views.generic import ListView, DetailView

from inventor.core.listings.filters import ListingFilter
from inventor.core.listings.models.listing_types import Accommodation
from pragmatic.mixins import LoginPermissionRequiredMixin

from inventor.core.listings.models.general import Listing


class ListingListView(LoginPermissionRequiredMixin, ListView):
    model = Listing
    filter_class = ListingFilter
    test = Accommodation
    permission_required = 'listings.list_listing'
    paginate_by = 12

    def dispatch(self, request, *args, **kwargs):
        self.filter = self.filter_class(request.GET, queryset=self.get_whole_queryset())
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.filter.qs.select_related('location')
        return queryset
        # return self.sort_queryset(queryset)

    def get_whole_queryset(self):
        return self.model.objects.order_by('-promoted', 'modified')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(*kwargs)
        context_data.update({
            'title': self.model._meta.verbose_name_plural,
            'filter': self.filter
        })
        return context_data


class ListingDetailView(LoginPermissionRequiredMixin, DetailView):
    model = Listing
    permission_required = 'listings.view_listing'

