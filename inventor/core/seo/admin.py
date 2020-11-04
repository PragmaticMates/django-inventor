from django.apps import apps
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from django.core.exceptions import ImproperlyConfigured

from modeltrans.admin import ActiveLanguageMixin

from inventor.core.seo.forms import SeoForm
from inventor.core.seo.models import Seo
from inventor.helpers import get_listing_types_classes
from inventor import settings


class SeoAdmin(ActiveLanguageMixin, admin.ModelAdmin):
    list_display = ['content_object', 'title_i18n', 'description_i18n', 'keywords_i18n']
    list_editable = ['title_i18n', 'description_i18n', 'keywords_i18n']

try:
    admin.site.register(Seo, SeoAdmin)
except admin.sites.AlreadyRegistered:
    pass


class SeoInlines(GenericStackedInline):
    model = Seo
    form = SeoForm
    extra = 1
    max_num = 1
    inlines = None


def register_model(model):
    try:
        model_admin = admin.site._registry[model].__class__
    except KeyError:
        raise ImproperlyConfigured("Please put ``seo`` in your settings.py only as last INSTALLED_APPS")
    admin.site.unregister(model)

    if not SeoInlines in model_admin.inlines:
        model_admin.inlines = list(model_admin.inlines)[:] + [SeoInlines]

    admin.site.register(model, model_admin)


for model_name in getattr(settings, 'SEO_FOR_MODELS', []):
    if model_name == 'Listing':
        for model in get_listing_types_classes():
            register_model(model)
    else:
        model = apps.get_model(model_name)
        register_model(model)
