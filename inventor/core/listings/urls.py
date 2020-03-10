from django.urls import path
from django.utils.text import slugify
from django.utils.translation import pgettext_lazy, ugettext_lazy

from inventor.core.listings.models.general import Listing
from inventor.core.listings.views import ListingListView, ListingDetailView

app_name = 'listings'

urlpatterns = [
    path(pgettext_lazy('url', 'listings/'), ListingListView.as_view(), name='listing_list'),
]

# lists
for listing_type in Listing.__subclasses__():
    url_name = listing_type.get_list_url_name()
    verbose_name_plural = ugettext_lazy(listing_type._meta.verbose_name_plural)
    url_path = slugify(verbose_name_plural) + '/'
    urlpatterns.append(path(url_path, ListingListView.as_view(template_name='listings/listing_list.html', model=listing_type), name=url_name))

# listing detail
urlpatterns.append(path(pgettext_lazy('url', '<str:slug>/'), ListingDetailView.as_view(), name='listing_detail'))
