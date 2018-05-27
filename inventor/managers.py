from django.db.models import Q
from model_utils.managers import InheritanceQuerySet


class ListingQuerySet(InheritanceQuerySet):
    def without_points(self):
        return self.filter(point=None)

    def with_points(self):
        return self.exclude(point=None)

    def with_address(self):
        return self.exclude(Q(street='') | Q(city='') | Q(country=''))

    def published(self):
        return self.filter(published=True)

    def not_published(self):
        return self.filter(published=False)
