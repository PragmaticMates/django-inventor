from django.urls import path
from django.utils.translation import pgettext_lazy

from inventor.core.listings.views import ListingListView, ListingDetailView

app_name = 'listings'

urlpatterns = [
    path(pgettext_lazy('url', 'items/<int:pk>/'), ListingDetailView.as_view(), name='listing_detail'),
    path(pgettext_lazy('url', 'items/'), ListingListView.as_view(), name='listing_list'),
]
