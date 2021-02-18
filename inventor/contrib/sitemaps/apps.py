from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


# These SiteMaps are will be available in Django 3.2
# Commit: https://github.com/django/django/commit/16218c20606d8cd89c5393970c83da04598a3e04
# Ticket: https://code.djangoproject.com/ticket/27395
class SiteMapsConfig(AppConfig):
    name = 'inventor.contrib.sitemaps'
    label = 'sitemaps_contrib'
    verbose_name = _("Site Maps")
    verbose_name_force_translation = _("Site Maps")
