from django.db import models
from django.utils.translation import ugettext_lazy as _
from inventor.core.bookings.mixins import BookingMixin
from inventor.core.lexicons.models import Amenity
from inventor.core.listings.models.general import Listing


class Accommodation(BookingMixin, Listing):
    section = _('travel')
    amenities = models.ManyToManyField(to=Amenity, verbose_name=_('amenities'), blank=True)
    # TODO: type: hotel, apartment, cottage
    # TODO: class: 1-5

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


class EatAndDrink(Listing):  # TODO
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
        verbose_name = _('travel')
        verbose_name_plural = _('travels')
        ordering = ('title',)


class Event(Listing):
    section = _('events')
    # concert, speech, conference

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
        ordering = ('title',)


class Goods(Listing):
    section = _('shopping')

    class Meta:
        verbose_name = _('goods')
        verbose_name_plural = _('goods')
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
