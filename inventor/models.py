from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.contrib.gis.db import models
from django.contrib.gis.db.models import Avg
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from internationalflavor.countries import CountryField
from inventor.managers import ListingQuerySet


# TODO: banner, opening hours, gallery (and albums), videos, meals and drinks, location, 360, social, faq, price, booking

class Listing(models.Model):
    SOCIAL_NETWORKS = ['Facebook', 'Twitter', 'Google', 'Instagram', 'Vimeo', 'YouTube', 'LinkedIn', 'Dribbble', 'Skype', 'Foursquare', 'Behance']  # TODO: move to settings

    # definition
    title = models.CharField(_('title'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True)

    # management
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('author'))
    published = models.BooleanField(_('published'), default=True)
    featured = models.BooleanField(_('featured'), default=False)

    # specification
    categories = models.ManyToManyField(to='inventor.Category', verbose_name=_('categories'), blank=True, related_name='listings_of_category')
    amenities = models.ManyToManyField(to='inventor.Amenity', verbose_name=_('amenities'), blank=True, related_name='listings_having_amenity')
    services = models.ManyToManyField(to='inventor.Service', verbose_name=_('services'), blank=True, related_name='listings_with_services')

    # address
    street = models.CharField(_('street'), max_length=200)
    postcode = models.CharField(_('postcode'), max_length=30, db_index=True)
    city = models.CharField(_('city'), max_length=50)
    country = CountryField(verbose_name=_('country'), db_index=True)
    point = models.PointField(_('point'), blank=True, null=True, default=None)

    # contact information
    phone = models.CharField(_('phone'), max_length=40, blank=True)
    email = models.EmailField(_('email'), blank=True)
    website = models.URLField(_('website'), max_length=400, blank=True)

    # social
    social_networks = ArrayField(verbose_name=_('social networks'),
        base_field=models.CharField(verbose_name=_('social network'), max_length=10, choices=[(network, network) for network in SOCIAL_NETWORKS]),
        size=len(SOCIAL_NETWORKS), blank=True)

    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    objects = ListingQuerySet.as_manager()

    class Meta:
        verbose_name = _('listing')
        verbose_name_plural = _('listings')
        ordering = ('title',)
        default_permissions = settings.DEFAULT_PERMISSIONS

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('inventor:listing_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('inventor:listing_update', args=(self.pk,))

    @property
    def address(self):
        return '{}, {} {}, {}'.format(self.street, self.postcode, self.city, self.country).strip(', ')

    @property
    def country_and_city(self):
        address_parts = [
            self.get_country_display(),
            self.city
        ]

        return ', '.join(address_parts).strip(' ,')

    @cached_property
    def rating(self):
        avg_rating = self.ratingcomment_set.aggregate(Avg('rating'))
        rating = avg_rating['rating__avg']
        if rating:
            rating = round(rating, 2)
        return rating


class Accommodation(Listing):
    class Meta:
        verbose_name = _('accommodation')
        verbose_name_plural = _('accommodations')
        ordering = ('title',)
        default_permissions = settings.DEFAULT_PERMISSIONS


class Restaurant(Listing):
    class Meta:
        verbose_name = _('restaurant or bar')
        verbose_name_plural = _('restaurants and bars')
        ordering = ('title',)
        default_permissions = settings.DEFAULT_PERMISSIONS


class Business(Listing):
    class Meta:
        verbose_name = _('business')
        verbose_name_plural = _('businesses')
        ordering = ('title',)
        default_permissions = settings.DEFAULT_PERMISSIONS


class Travel(Listing):
    section = _('tourism')

    class Meta:
        verbose_name = _('travel')
        verbose_name_plural = _('travels')
        ordering = ('title',)
        default_permissions = settings.DEFAULT_PERMISSIONS


class Event(Listing):
    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
        ordering = ('title',)
        default_permissions = settings.DEFAULT_PERMISSIONS


class Shop(Listing):
    class Meta:
        verbose_name = _('shop')
        verbose_name_plural = _('shops')
        ordering = ('title',)
        default_permissions = settings.DEFAULT_PERMISSIONS


class Goods(Listing):
    class Meta:
        verbose_name = _('goods')
        verbose_name_plural = _('goods')
        ordering = ('title',)
        default_permissions = settings.DEFAULT_PERMISSIONS


class Vehicle(Listing):
    section = _('automotive')

    class Meta:
        verbose_name = _('vehicle')
        verbose_name_plural = _('vehicle')
        ordering = ('title',)
        default_permissions = settings.DEFAULT_PERMISSIONS


class Person(Listing):
    section = _('dating')

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('persons')
        ordering = ('title',)
        default_permissions = settings.DEFAULT_PERMISSIONS


class Course(Listing):
    section = _('education')

    class Meta:
        verbose_name = _('course')
        verbose_name_plural = _('courses')
        ordering = ('title',)
        default_permissions = settings.DEFAULT_PERMISSIONS


class Animal(Listing):
    class Meta:
        verbose_name = _('animal')
        verbose_name_plural = _('animals')
        ordering = ('title',)
        default_permissions = settings.DEFAULT_PERMISSIONS


class Category(models.Model):
    title = models.CharField(_('title'), max_length=100, unique=True)

    # TODO: listing types
    # listing_types = ArrayField(verbose_name=_('listing types'),
    #                        base_field=models.CharField(verbose_name=_('listing type'), max_length=10,
    #                                                    choices=Listing.TYPES),
    #                        size=len(Listing.TYPES),
    #                        blank=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('title',)
        default_permissions = settings.DEFAULT_PERMISSIONS

    def __str__(self):
        return self.title


class Amenity(models.Model):
    title = models.CharField(_('name'), max_length=100, unique=True)

    # TODO: listing types

    class Meta:
        verbose_name = _('amenity')
        verbose_name_plural = _('amenities')
        ordering = ('title',)
        default_permissions = settings.DEFAULT_PERMISSIONS

    def __str__(self):
        return self.title


class Service(models.Model):
    title = models.CharField(_('name'), max_length=100, unique=True)

    # TODO: listing types

    class Meta:
        verbose_name = _('service')
        verbose_name_plural = _('services')
        ordering = ('title',)
        default_permissions = settings.DEFAULT_PERMISSIONS

    def __str__(self):
        return self.title


# from .signals import *
