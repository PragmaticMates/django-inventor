from django.views.generic import ListView, DetailView
from pragmatic.mixins import LoginPermissionRequiredMixin

from inventor.core.listings.models.general import Listing


class ListingListView(LoginPermissionRequiredMixin, ListView):
    model = Listing
    permission_required = 'listings.list_listing'


class ListingDetailView(LoginPermissionRequiredMixin, DetailView):
    model = Listing
    permission_required = 'listings.view_listing'

