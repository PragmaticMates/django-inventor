from django.conf import settings
from django.contrib.gis.db import models
from django.core.validators import MinValueValidator, EMPTY_VALUES
from django.db import transaction
from django.template.defaultfilters import date
from django.utils import timezone
from django.utils.translation import gettext_lazy as _, override as override_language

from inventor.core.bookings.querysets import BookingQuerySet
from pragmatic.managers import EmailManager

from inventor import settings as inventor_settings
from inventor.core.listings.models.general import Listing
from inventor.utils import generate_hash


class Booking(models.Model):
    HASH_KEY_LENGTH = 40
    STATUS_AWAITING_APPROVAL = 'AWAITING_APPROVAL'
    STATUS_PENDING_PAYMENT = 'PENDING_PAYMENT'
    STATUS_APPROVED = 'APPROVED'
    STATUS_CANCELLED = 'CANCELLED'
    STATUS_NO_SHOW = 'NO_SHOW'
    STATUS_COMPLETED = 'COMPLETED'
    STATUSES = [
        (STATUS_AWAITING_APPROVAL, _('Awaiting approval')),
        (STATUS_PENDING_PAYMENT, _('Pending payment')),
        (STATUS_APPROVED, _('Approved')),
        (STATUS_CANCELLED, _('Cancelled')),
        (STATUS_NO_SHOW, _('No-show')),
        (STATUS_COMPLETED, _('Completed')),
    ]
    status = models.CharField(verbose_name=_('status'), choices=STATUSES, max_length=17, default=STATUS_AWAITING_APPROVAL)
    traveler = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name=_('traveler'),
                                 blank=True, null=True, default=None)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, verbose_name=_('listing'))
    hash_key = models.CharField(verbose_name=_('hash key'), max_length=HASH_KEY_LENGTH, db_index=True, unique=True)
    book_from = models.DateTimeField(_('book from'), blank=True, null=True, default=None)
    book_to = models.DateTimeField(_('book to'), blank=True, null=True, default=None)
    number_of_persons = models.PositiveSmallIntegerField(_('number of persons'), blank=True, null=True, default=None)
    price = models.DecimalField(_('price'), help_text=inventor_settings.CURRENCY, max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],
                                blank=True, null=True, default=None)
    message = models.TextField(_('message'), blank=True)

    # contact information
    person = models.CharField(_('person'), max_length=100, blank=True)
    phone = models.CharField(_('phone'), max_length=40, blank=True)
    email = models.EmailField(_('email'), blank=True)

    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    objects = BookingQuerySet.as_manager()

    class Meta:
        verbose_name = _('booking')
        verbose_name_plural = _('bookings')
        ordering = ('-created',)
        get_latest_by = 'created'

    def __str__(self):
        return f'#{self.id}'

    @staticmethod
    def generate_hash_key():
        while True:
            hash = generate_hash(length=Booking.HASH_KEY_LENGTH)

            if not Booking.objects.filter(hash_key=hash).exists():
                break

        return hash

    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.hash_key in EMPTY_VALUES:
            self.hash_key = Booking.generate_hash_key()

        return super().save(*args, **kwargs)

    def get_date_display(self):
        book_from = self.get_book_from_display()
        book_to = self.get_book_from_display()

        if book_from != book_to:
            return f'{book_from} - {book_to}'

        return book_from

    def get_book_from_display(self):
        # TODO: check booking date settings of listing (or type)
        current_tz = timezone.get_current_timezone()
        return date(self.book_from.astimezone(current_tz), settings.DATE_FORMAT)

    def get_book_to_display(self):
        # TODO: check booking date settings of listing (or type)
        current_tz = timezone.get_current_timezone()
        return date(self.book_to.astimezone(current_tz), settings.DATE_FORMAT)

    def send_request(self):
        # send message to owner
        with override_language(self.listing.author.preferred_language):
            # TODO: notify using whistle
            EmailManager.send_mail(
                to=self.listing.author,
                template_prefix='bookings/mails/booking_request',
                subject='%s #%d' % (_('Booking request'), self.id),
                data={'booking': self},
                reply_to=self.email,
                request=None
            )
