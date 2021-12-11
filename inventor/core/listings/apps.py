from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'inventor.core.listings'
    verbose_name = _('Listings')

    def ready(self):
        self.register_comments()
        self.register_discounts()

    def register_comments(self):
        from django_comments.moderation import moderator
        from inventor.contrib.comments.moderation import ListingCommentModerator
        from inventor.helpers import get_listing_types_classes

        for model in get_listing_types_classes():
            moderator.register(model, ListingCommentModerator)

    def register_discounts(self):
        from commerce.models import Discount
        from inventor.core.listings.models.general import Listing
        Discount.products.add_relation(Listing)
