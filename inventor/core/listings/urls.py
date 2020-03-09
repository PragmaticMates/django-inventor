from django.urls import path
from django.utils.translation import pgettext_lazy

from inventor.core.listings.models.listing_types import Accommodation
from inventor.core.listings.views import ListingListView, ListingDetailView

app_name = 'listings'

urlpatterns = [
    path(pgettext_lazy('url', 'listings/'), ListingListView.as_view(), name='listing_list'),
    path(pgettext_lazy('url', 'accommodations/'), ListingListView.as_view(model=Accommodation), name='accommodation_list'),
    path(pgettext_lazy('url', '<str:slug>/'), ListingDetailView.as_view(), name='listing_detail'),
]
