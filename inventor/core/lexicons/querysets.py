from django.contrib.contenttypes.models import ContentType
from mptt.managers import TreeManager


class CategoryManager(TreeManager):
    def of_listing_type(self, listing_type):
        return self.filter(listing_type=ContentType.objects.get_for_model(listing_type))
