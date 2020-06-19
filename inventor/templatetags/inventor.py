from django import template
from django.contrib.auth import get_user_model

from inventor.core.lexicons.models import Category
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


@register.simple_tag
def inventor_faqs(**kwargs):
    from inventor.core.faqs.models import FAQ
    return FAQ.objects.all()


@register.simple_tag
def inventor_partners(**kwargs):
    from inventor.core.partners.models import Partner
    return Partner.objects.all()


@register.simple_tag
def inventor_stats(stat):
    if stat == 'purchased_listings':
        return 'TODO'
    if stat == 'active_users':
        return get_user_model().objects.active().count()
    if stat == 'published_listings':
        return Listing.objects.published().count()
    if stat == 'categories':
        return Category.objects.count()

    return None
