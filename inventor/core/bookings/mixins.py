from django.db import models
from django.utils.translation import ugettext_lazy as _


class BookingMixin(models.Model):
    PERIODS = [  # TODO: deprecated? should be replaced by listing price?
        ('HOUR', _('hour')),
        ('DAY', _('day')),
        ('NIGHT', _('night')),
    ]
    booking_enabled = models.BooleanField(_('bookings enabled'), default=True)
    booking_url = models.URLField(_('booking URL'), max_length=300,
                                  blank=True)
    booking_period = models.CharField(_('booking period'), choices=PERIODS, max_length=5, blank=True)
    booking_min_period = models.SmallIntegerField(verbose_name=_('min period'),
                                                   blank=True, null=True, default=None)
    booking_max_period = models.SmallIntegerField(verbose_name=_('max period'),
                                                   blank=True, null=True, default=None)
    booking_min_persons = models.SmallIntegerField(verbose_name=_('min persons'),
                                                    blank=True, null=True, default=None)
    # booking_max_persons = models.SmallIntegerField(verbose_name=_('max persons'),
    #                                                 blank=True, null=True, default=None)
    capacity = models.SmallIntegerField(verbose_name=_('capacity'),
        blank=True, null=True, default=None)

    class Meta:
        abstract = True
