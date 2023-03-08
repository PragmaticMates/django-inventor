from django.db.models import Q, F, Count
from model_utils.managers import InheritanceQuerySet


class ListingQuerySet(InheritanceQuerySet):
    def without_points(self):
        return self.filter(point=None)

    def with_points(self):
        return self.exclude(point=None)

    def without_price(self):
        return self.filter(price=None)

    def with_price(self):
        return self.exclude(price=None)
    
    def with_address(self):
        return self.exclude(Q(street='') | Q(city='') | Q(country=''))

    def published(self):
        return self.filter(published=True)

    def not_published(self):
        return self.filter(published=False)

    def hidden(self):
        return self.filter(hidden=True)

    def not_hidden(self):
        return self.filter(hidden=False)

    def promoted(self):
        return self.filter(promoted=True)

    def not_promoted(self):
        return self.filter(promoted=False)

    def of_categories(self, categories, deep=True):
        filter_categories = categories

        if deep:
            filter_categories = []

            for category in categories:
                desc = category.get_descendants(include_self=True)
                ids = desc.values_list('id', flat=True)
                filter_categories += ids

        return self.filter(categories__in=filter_categories)

    def of_category(self, category, deep=True):
        if deep:
            return self.filter(categories__in=category.get_descendants(include_self=True))
        return self.filter(categories=category)

    def by_keyword(self, keyword):
        return self.filter(
            Q(title_i18n__unaccent__icontains=keyword) |
            Q(description_i18n__unaccent__icontains=keyword)
        )

    def with_annotations(self):
        return self.annotate(
            locality_title=F('locality__title'),
            favorite_of_users__count=Count('favorite_of_users')
        )

    def with_prefetched(self):
        return self.prefetch_related('categories', 'groups')

    def select_subclasses(self, *subclasses):
        if not subclasses:
            from inventor.helpers import get_listing_types_classes
            subclasses = get_listing_types_classes()

        return super().select_subclasses(*subclasses)
