from allauth.utils import build_absolute_uri
from django import template
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.template import TemplateDoesNotExist
from filer.models import File
from inventor.core.lexicons.models import Category
from inventor.core.listings.models.general import Listing
from inventor.core.listings.models.listing_types import Race

register = template.Library()


@register.simple_tag
def inventor_listings(**kwargs):
    return Listing\
        .objects\
        .published()\
        .not_hidden()\
        .select_subclasses()\
        .prefetch_related('categories')\
        .order_by('-promoted', 'awaiting', 'created')


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
