from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'inventor.core.listings'
    verbose_name = _('Listings')

    def ready(self):
        from commerce.models import Discount
        from inventor.core.listings.models.general import Listing
        Discount.products.add_relation(Listing)
