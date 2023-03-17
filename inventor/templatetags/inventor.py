from allauth.utils import build_absolute_uri
from django import template
from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.template import TemplateDoesNotExist
from filer.models import File
from mptt.forms import TreeNodeChoiceField, TreeNodeMultipleChoiceField

from inventor.core.lexicons.models import Category
from inventor.core.listings.models.general import Listing
from inventor.core.listings.models.listing_types import Race

register = template.Library()


@register.simple_tag(takes_context=True)
def inventor_listings(context, proxy='all', listing_type=None, limit=None):
    if listing_type:
        listing_type_class = apps.get_model(f'listings.{listing_type}')
    else:
        listing_type_class = Listing

    listings = listing_type_class.objects \
        .published() \
        .not_hidden() \
        .annotate(Count('favorite_of_users')) \
        .prefetch_related('categories')

    if listing_type_class == Listing:
        listings = listings.select_subclasses()

    if proxy == 'all':
        listings = listings.order_by('-promoted', '-rank', '-created')

    if proxy == 'recommended':
        listings = listings \
            .filter(favorite_of_users__count__gt=0)\
            .order_by('-favorite_of_users__count')

    if proxy == 'not_purchased' and 'commerce' in settings.INSTALLED_APPS:
        from commerce.models import PurchasedItem
        user = context.get('user', None)
        purchased_items = PurchasedItem.objects\
            .of_not_cancelled_nor_refunded_orders()\
            .filter(order__user=user)\
            .values_list('object_id', flat=True)  # TODO: gm2m with content_type
        listings = listings.exclude(id__in=list(purchased_items))

    if proxy == 'favorites':
        user = context.get('user', None)
        listings = listings.filter(id__in=user.favorite_listings.all()) if user else Listing.objects.none()

    if limit:
        listings = listings[:limit]

    return listings


@register.simple_tag
def inventor_faqs(**kwargs):
    from inventor.core.faqs.models import FAQ
    return FAQ.objects.all()


@register.simple_tag
def inventor_partners(**kwargs):
    from inventor.core.partners.models import Partner
    return Partner.objects.all()


@register.simple_tag
def inventor_plans(**kwargs):
    from inventor.core.subscriptions.models import Plan
    return Plan.objects.all()


@register.simple_tag
def inventor_stats(stat):
    if stat == 'approved_files':
        return File.objects.filter(folder__name='approved').count()  # TODO: move to settings
    if stat == 'active_users':
        return get_user_model().objects.active().count()
    if stat == 'published_listings':
        return Listing.objects.published().not_hidden().count()
    if stat == 'published_races':  # TODO: filter listings by argument
        return Race.objects.published().not_hidden().count()
    if stat == 'categories':
        return Category.objects.count()

    return None


@register.simple_tag(takes_context=True)
def uri(context, location):
    try:
        return build_absolute_uri(context.get('request', None), location)
    except ObjectDoesNotExist:
        return location


@register.filter()
def listing_template(obj):
    prefix = obj.__class__.__name__.lower()
    suffix = '_item'
    template_name = f'listings/widgets/{prefix}{suffix}.html'

    try:
        template.loader.get_template(template_name)
        return template_name
    except TemplateDoesNotExist:
        return f'listings/widgets/listing{suffix}.html'


@register.simple_tag
def get_choices_with_parents(**kwargs):
    field = kwargs.get('field', None)

    if not isinstance(field, TreeNodeMultipleChoiceField) and not isinstance(field, TreeNodeChoiceField):
        return None

    return dict(field.queryset.values_list(field.to_field_name or 'id', 'parent'))


@register.filter()
def has_choice_children(choices_with_parents, choice):
    current_parent = choices_with_parents.get(choice, None)
    next_choice = _get_next_choice(choice, choices_with_parents)
    next_parent = choices_with_parents.get(next_choice, None) if next_choice else None

    return current_parent is None and next_parent is not None


@register.filter()
def is_last_child(choices_with_parents, choice):
    current_parent = choices_with_parents.get(choice, None)
    next_choice = _get_next_choice(choice, choices_with_parents)
    next_parent = choices_with_parents.get(next_choice, None) if next_choice else None
    choices_has_any_parent = None in choices_with_parents.values()

    return current_parent is not None and next_parent is None and choices_has_any_parent


def _get_next_choice(choice, choices_with_parents):
    choices = list(choices_with_parents)
    try:
        next_choice = choices[choices.index(choice) + 1]
    except (ValueError, IndexError):
        next_choice = None
    return next_choice
