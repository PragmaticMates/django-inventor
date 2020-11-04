from django import template
from django.core.validators import EMPTY_VALUES

from inventor.core.seo.models import Seo

register = template.Library()


@register.simple_tag(takes_context=True)
def seo(context):
    view = context.get('view', None)
    obj = context.get('object', None)

    s = {}
    look = []

    if view:
        look.append(view)

    if obj:
        look = [obj] + look
        seo = Seo.objects.for_object(obj)

        if seo:
            look = [seo] + look

    for meta in ['title', 'description', 'keywords', 'robots']:
        for l in look:
            attr_name = f'{meta}_i18n' if isinstance(l, Seo) and meta != 'robots' else meta
            attr = getattr(l, attr_name, '')
            if attr not in EMPTY_VALUES:
                s[meta] = attr
                break
            elif attr_name == 'robots' and getattr(l, 'hidden', False):
                s[meta] = 'noindex'

    return s
