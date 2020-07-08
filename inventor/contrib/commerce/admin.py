# from django.contrib import admin
# from django.contrib.contenttypes.admin import GenericStackedInline
# from django.core.exceptions import ImproperlyConfigured
# 
# from commerce.models import Supply
# from inventor.helpers import get_listing_types_classes


# # for model_name in getattr(settings, 'SUPPLY_FOR_MODELS', []):
# for model in get_listing_types_classes():
#     try:
#         model_admin = admin.site._registry[model].__class__
#     except KeyError:
#         raise ImproperlyConfigured("Please put ``inventor.contrib.commerce`` in your settings.py as last in INSTALLED_APPS")
#     admin.site.unregister(model)
#
#     if not SupplyInline in model_admin.inlines:
#         model_admin.inlines = list(model_admin.inlines)[:] + [SupplyInline]
#
#     admin.site.register(model, model_admin)
