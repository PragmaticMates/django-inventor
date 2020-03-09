from django.contrib.postgres.fields import DateTimeRangeField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from inventor.core.bookings.mixins import BookingMixin
from inventor.core.lexicons.models import AccommodationAmenity
from inventor.core.listings.models.general import Listing


class Accommodation(BookingMixin, Listing):
    # Apartmán
    # Chata v prírode
    # Dovolenkový dom
    # Horská chata
    # Hotel
    # Hostel
    # Penzión
    # Privát
    # Resort

    section = _('travel')  # ?
    amenities = models.ManyToManyField(to=AccommodationAmenity, verbose_name=_('amenities'), blank=True)
    # type = models.ForeignKey( # TODO: Deprecated - replaced by categories
    #     AccommodationType, verbose_name=_('type'), on_delete=models.SET_NULL, related_name='type',
    #     blank=True, null=True, default=None)
    star_rating = models.SmallIntegerField(
        verbose_name=_('Star rating'), validators=[MinValueValidator(1), MaxValueValidator(5)],
        blank=True, null=True, default=None)
    rooms = models.SmallIntegerField(
        verbose_name=_('number of rooms'), validators=[MinValueValidator(1)],
        blank=True, null=True, default=None)

    class Meta:
        verbose_name = _('accommodation')
        verbose_name_plural = _('accommodations')
        ordering = ('title',)


class Property(Listing):
    section = _('real estate')
    # TODO: type: business, house, flat, area?

    class Meta:
        verbose_name = _('property')
        verbose_name_plural = _('properties')
        ordering = ('title',)


class EatAndDrink(BookingMixin, Listing):  # TODO
    section = _('gastronomy')
    # type: restaurant, cafe, pub, bistro, fast-food

    class Meta:
        verbose_name = _('eat & drink')
        verbose_name_plural = _('eat & drinks')
        ordering = ('title',)


class Service(Listing):
    section = _('services')
    # barber, taxi, haircut, shop

    class Meta:
        verbose_name = _('service')
        verbose_name_plural = _('services')
        ordering = ('title',)


class Vacation(Listing):  # Relax/Vacation
    section = _('tourism')

    class Meta:
        verbose_name = _('vacation')
        verbose_name_plural = _('vacations')
        ordering = ('title',)


class Event(Listing):
    section = _('events')
    # concert, speech, conference

    date = DateTimeRangeField(_('datetime range'), db_index=True,
                              blank=True, null=True, default=None)

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
        ordering = ('title',)


class Shop(Listing):  # Store
    section = _('shopping')

    class Meta:
        verbose_name = _('shop')
        verbose_name_plural = _('shops')
        ordering = ('title',)


class Vehicle(Listing):
    section = _('automotive')

    class Meta:
        verbose_name = _('vehicle')
        verbose_name_plural = _('vehicle')
        ordering = ('title',)


class Profile(Listing):
    section = _('dating')

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')
        ordering = ('title',)


class Job(Listing):
    section = _('work')

    class Meta:
        verbose_name = _('job')
        verbose_name_plural = _('jobs')
        ordering = ('title',)


class Course(Listing):
    section = _('education')

    class Meta:
        verbose_name = _('course')
        verbose_name_plural = _('courses')
        ordering = ('title',)


class Nature(Listing):
    section = _('flora and fauna')
    #type = animal, plant

    class Meta:
        verbose_name = _('animal or plant')
        verbose_name_plural = _('animals and plants')
        ordering = ('title',)
