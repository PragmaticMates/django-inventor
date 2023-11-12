from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'inventor.manager.bookings'
    label = 'manager_bookings'
    verbose_name = _('Bookings')
