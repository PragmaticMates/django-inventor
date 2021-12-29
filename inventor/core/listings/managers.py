from django.db.models import Q
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

    def of_category(self, category, deep=True):
        # TODO: more nested categories
        slugs = [category.slug_i18n]

        if deep and category.parent:
            slugs.append(category.parent.slug_i18n)

        return self.by_category_slugs(slugs, deep)

    def by_category_slugs(self, slugs, deep=True):
        # TODO: more nested categories
        return self.filter(
            Q(categories__slug_i18n__in=slugs) |
            Q(categories__parent__slug_i18n__in=slugs)
        ) if deep else self.filter(categories__slug_i18n__in=slugs)

    def by_keyword(self, keyword):
        return self.filter(
            Q(title_i18n__unaccent__icontains=keyword) |
            Q(description_i18n__unaccent__icontains=keyword)
        )

    def select_subclasses(self, *subclasses):
        if not subclasses:
            from inventor.helpers import get_listing_types_classes
            subclasses = get_listing_types_classes()

        return super().select_subclasses(*subclasses)
