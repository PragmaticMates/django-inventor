from django import template
from inventor.core.listings.models.general import Listing

register = template.Library()


@register.simple_tag
def inventor_listings(**kwargs):
    return Listing\
        .objects\
        .published()\
        .select_subclasses()\
        .prefetch_related('categories')\
        .order_by('-promoted', 'created')
