from django import template
from django.conf import settings
from django.core.validators import EMPTY_VALUES
from django.db.models.fields.files import ImageFieldFile

from inventor.core.seo.models import Seo

register = template.Library()


@register.simple_tag(takes_context=True)
def seo(context):
    request = context['request']
    path = request.path
    obj = context.get('object', None)
    view = context.get('view', None)

    subjects = [path, obj, view]
    s = {}
    look = []

    for subject in subjects:
        if subject:
            seo = Seo.objects.for_subject(subject)

            if seo:
                look.append(seo)

            if not isinstance(subject, str):
                look.append(subject)

    for meta in ['title', 'description', 'keywords', 'robots', 'image']:
        for l in look:
            attr_name = f'{meta}_i18n' if isinstance(l, Seo) and meta not in ['robots', 'image'] else meta
            attr = getattr(l, attr_name, '')

            if attr not in EMPTY_VALUES:
                s[meta] = attr
                break
            elif attr_name == 'robots' and getattr(l, 'hidden', False):
                s[meta] = 'noindex'

    # image
    image = s.get('image', None)
    if image and isinstance(image, ImageFieldFile):
        s.update({
            'image': image.url,
            'image_width': image.width,
            'image_height': image.height
        })
    elif not image and getattr(settings, 'PAGE_IMAGE', None):
        s.update({
            'image': settings.PAGE_IMAGE,
        })

    # locale
    s.update({
        'locale': request.LANGUAGE_CODE,
    })

    # from pprint import pprint
    # pprint(s)

    # TODO: cache
    return s
