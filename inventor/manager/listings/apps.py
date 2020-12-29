from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'inventor.manager.listings'
    label = 'manager.listings'
    verbose_name = _('Listings')
