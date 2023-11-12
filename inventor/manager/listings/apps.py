from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class Config(AppConfig):
    name = 'inventor.manager.listings'
    label = 'manager_listings'
    verbose_name = _('Listings')
