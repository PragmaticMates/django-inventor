from django import template
from django.core.validators import EMPTY_VALUES

from inventor.core.seo.models import Seo

register = template.Library()


@register.simple_tag(takes_context=True)
def seo(context):
    request = context['request'].path
    obj = context.get('object', None)
    view = context.get('view', None)

    subjects = [request, obj, view]
    s = {}
    look = []

    for subject in subjects:
        if subject:
            if not isinstance(subject, str):
                look.append(subject)

            seo = Seo.objects.for_subject(subject)

            if seo:
                look.append(seo)

    for meta in ['title', 'description', 'keywords', 'robots']:
        for l in look:
            attr_name = f'{meta}_i18n' if isinstance(l, Seo) and meta != 'robots' else meta
            attr = getattr(l, attr_name, '')
            if attr not in EMPTY_VALUES:
                s[meta] = attr
                break
            elif attr_name == 'robots' and getattr(l, 'hidden', False):
                s[meta] = 'noindex'

    # TODO: cache
    return s
