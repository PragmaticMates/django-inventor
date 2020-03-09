from django.views.generic import ListView, DetailView

from inventor.core.listings.models.listing_types import Accommodation
from pragmatic.mixins import LoginPermissionRequiredMixin

from inventor.core.listings.models.general import Listing


class ListingListView(LoginPermissionRequiredMixin, ListView):
    model = Listing
    test = Accommodation
    permission_required = 'listings.list_listing'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(*kwargs)
        context_data.update({
            'title': self.model._meta.verbose_name_plural,
        })
        return context_data


class ListingDetailView(LoginPermissionRequiredMixin, DetailView):
    model = Listing
    permission_required = 'listings.view_listing'

