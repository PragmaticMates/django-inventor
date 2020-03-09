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

    def promoted(self):
        return self.filter(promoted=True)

    def not_promoted(self):
        return self.filter(promoted=False)

    def by_keyword(self, keyword):
        return self.filter(
            Q(title__unaccent__icontains=keyword) |
            Q(description__unaccent__icontains=keyword)
        )
