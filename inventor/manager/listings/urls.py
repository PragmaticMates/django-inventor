from django.urls import path
from django.utils.translation import pgettext_lazy

from inventor import settings as inventor_settings
from inventor.core.listings.models.general import Listing
from inventor.manager.listings.views import ListingListView, ListingStatsView

app_name = 'manager_listings'

urlpatterns = []


# if inventor_settings.LISTINGS_URL_ENABLED:
urlpatterns.append(path(pgettext_lazy('url', 'listings/'), ListingListView.as_view(), name='listing_list'))


# lists
for index, listing_type in enumerate(Listing.__subclasses__()):
    url_name = listing_type.get_list_url_name()
    url_path = listing_type.URL.slug
    urlpatterns.append(path(url_path, ListingListView.as_view(model=listing_type), name=url_name))

    if not inventor_settings.LISTINGS_URL_ENABLED and len(inventor_settings.LISTING_TYPES) > 0 and listing_type.__name__ == inventor_settings.LISTING_TYPES[0]:
        urlpatterns.append(path(url_path, ListingListView.as_view(model=listing_type), name='listing_list'))

# listing detail
urlpatterns.append(path(pgettext_lazy('url', '<str:slug>/stats/'), ListingStatsView.as_view(), name='listing_stats'))
urlpatterns.append(path(pgettext_lazy('url', '<str:slug>/info/'), ListingStatsView.as_view(), name='listing_info'))
urlpatterns.append(path(pgettext_lazy('url', '<str:slug>/bookings/'), ListingStatsView.as_view(), name='listing_bookings'))
urlpatterns.append(path(pgettext_lazy('url', '<str:slug>/gallery/'), ListingStatsView.as_view(), name='listing_gallery'))
urlpatterns.append(path(pgettext_lazy('url', '<str:slug>/reviews/'), ListingStatsView.as_view(), name='listing_reviews'))
urlpatterns.append(path(pgettext_lazy('url', '<str:slug>/seo/'), ListingStatsView.as_view(), name='listing_seo'))
