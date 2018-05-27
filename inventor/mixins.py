from django.db import models
from django.utils.translation import ugettext_lazy as _


class BookingMixin(object):
    capacity = models.SmallIntegerField(verbose_name=_('capacity'),
        blank=True, null=True, default=None)
