from django.contrib.contenttypes.models import ContentType
from django.db import models


class CategoryQuerySet(models.QuerySet):
    def of_listing_type(self, listing_type):
        return self.filter(listing_type=ContentType.objects.get_for_model(listing_type))
