from django.db import models
from django.utils.translation import ugettext_lazy as _


class BookingMixin(models.Model):
    PERIODS = [  # TODO: deprecated? should be replaced by listing price?
        ('HOUR', _('hour')),
        ('DAY', _('day')),
        ('NIGHT', _('night')),
    ]
    bookings_enabled = models.BooleanField(_('bookings enabled'), default=True)
    booking_period = models.CharField(_('booking period'), choices=PERIODS, max_length=5, blank=True)
    bookings_min_period = models.SmallIntegerField(verbose_name=_('min period'),
                                                   blank=True, null=True, default=None)
    bookings_max_period = models.SmallIntegerField(verbose_name=_('max period'),
                                                   blank=True, null=True, default=None)
    bookings_min_persons = models.SmallIntegerField(verbose_name=_('min persons'),
                                                    blank=True, null=True, default=None)
    # bookings_max_persons = models.SmallIntegerField(verbose_name=_('max persons'),
    #                                                 blank=True, null=True, default=None)
    capacity = models.SmallIntegerField(verbose_name=_('capacity'),
        blank=True, null=True, default=None)

    class Meta:
        abstract = True
