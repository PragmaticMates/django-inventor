from django.conf.urls import url
from django.utils.translation import pgettext_lazy

from inventor.core.listings.views import ListingListView

app_name = 'listings'

urlpatterns = [
    url(pgettext_lazy("url", r'^items/$'), ListingListView.as_view(), name='listing_list'),
]
