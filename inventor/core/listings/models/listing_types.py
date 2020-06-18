from django.contrib.postgres.fields import DateTimeRangeField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from sorl import thumbnail

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


class Vacation(Listing):
    section = _('holiday')

    class Meta:
        verbose_name = _('vacation')
        verbose_name_plural = _('vacations')
        ordering = ('title',)


class Activity(Listing):
    section = _('relax')

    class Meta:
        verbose_name = _('activity')
        verbose_name_plural = _('activities')
        ordering = ('title',)


class Race(Listing):
    section = _('sport')
    distance = models.PositiveSmallIntegerField(_('distance'), help_text='km', blank=True, null=True, default=None)
    # date = models.DateField(_('date'), blank=True, null=True, default=None)  # TODO: range field?
    medal = thumbnail.ImageField(
        verbose_name=_('medal'),
        help_text=_('photo or image'),
        max_length=1024,
        upload_to='images',
        blank=True
    )

    class Meta:
        verbose_name = _('race')
        verbose_name_plural = _('races')
        ordering = ('title',)

    def get_distance_display(self):
        return f'{self.distance} km' if self.distance else ''


class Training(Listing):
    section = _('health & body')

    class Meta:
        verbose_name = _('training')
        verbose_name_plural = _('trainings')
        ordering = ('title',)


class Exercise(Listing):
    section = _('health & body')
    difficulty = models.PositiveSmallIntegerField(_('difficulty'), blank=True, null=True, default=None, validators=[MaxValueValidator(10)])
    duration = models.PositiveSmallIntegerField(_('duration'), help_text='min', blank=True, null=True, default=None)

    class Meta:
        verbose_name = _('exercise')
        verbose_name_plural = _('exercises')
        ordering = ('title',)

    def get_duration_display(self):
        return f'{self.duration} min' if self.duration else ''


class Trip(Listing):
    section = _('tourism')
    distance = models.PositiveSmallIntegerField(_('distance'), help_text='km', blank=True, null=True, default=None)

    class Meta:
        verbose_name = _('trip')
        verbose_name_plural = _('trips')
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


class Product(Listing):  # e-shop
    section = _('shopping')
    # TODO: size [lexicon]
    # TODO: color [lexicon]

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ('title',)
