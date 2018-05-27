import os
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import ArrayField
from django.contrib.gis.db import models
from django.contrib.gis.db.models import Avg
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django_comments import get_model as get_comment_model
from internationalflavor.countries import CountryField
from inventor import settings as inventor_settings
from inventor.managers import ListingQuerySet
from inventor.mixins import BookingMixin


# TODO: opening hours, meals and drinks, street view, faq

class Listing(models.Model):
    SOCIAL_NETWORKS = ['Facebook', 'Twitter', 'Google', 'Instagram', 'Vimeo', 'YouTube', 'LinkedIn', 'Dribbble',
                       'Skype', 'Foursquare', 'Behance']  # TODO: move to settings

    PRICE_UNITS = [
        ('PERSON', _('person')),
        ('NIGHT', _('night')),
        ('DAY', _('day')),
    ]

    # definition
    title = models.CharField(_('title'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True)

    # management
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('author'))
    published = models.BooleanField(_('published'), default=True)
    promoted = models.BooleanField(_('promoted'), default=False)

    # specification
    categories = models.ManyToManyField(to='inventor.Category', verbose_name=_('categories'), blank=True, related_name='listings_of_category')
    amenities = models.ManyToManyField(to='inventor.Amenity', verbose_name=_('amenities'), blank=True, related_name='listings_having_amenity')
    features = models.ManyToManyField(to='inventor.Feature', verbose_name=_('features'), blank=True, related_name='listings_with_features')

    # price
    price_starts_at = models.BooleanField(_('price starts at'), default=False)
    price = models.DecimalField(_('price'), help_text=inventor_settings.CURRENCY, max_digits=10, decimal_places=2, db_index=True, validators=[MinValueValidator(0)],
        blank=True, null=True, default=None)
    price_unit = models.CharField(_('price per unit'), choices=PRICE_UNITS, max_length=6, blank=True)

    # address
    location = models.ForeignKey('inventor.Location', on_delete=models.SET_NULL,
        blank=True, null=True, default=None)
    street = models.CharField(_('street'), max_length=200)
    postcode = models.CharField(_('postcode'), max_length=30, db_index=True)
    city = models.CharField(_('city'), max_length=50)
    country = CountryField(verbose_name=_('country'), db_index=True)
    point = models.PointField(_('point'), blank=True, null=True, default=None)

    # previews
    image = models.ImageField(
        verbose_name=_('image'),
        help_text=_('photo or image'),
        max_length=1024,
        upload_to='images',
    )

    banner = models.ImageField(
        verbose_name=_('banner'),
        help_text=_('photo or image'),
        max_length=1024 * 5,
        upload_to='banners',
    )

    # contact information
    phone = models.CharField(_('phone'), max_length=40, blank=True)
    email = models.EmailField(_('email'), blank=True)
    website = models.URLField(_('website'), max_length=400, blank=True)

    # social
    social_networks = ArrayField(verbose_name=_('social networks'),
        base_field=models.CharField(verbose_name=_('social network'), max_length=10, choices=[(network, network) for network in SOCIAL_NETWORKS]),
        size=len(SOCIAL_NETWORKS), blank=True)

    # gallery
    photos = GenericRelation('inventor.Photo', content_type_field='content_type', object_id_field='object_id', related_query_name='listing')
    comments = GenericRelation(get_comment_model(), content_type_field='content_type', object_id_field='object_pk',
                               related_query_name='contest')

    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    objects = ListingQuerySet.as_manager()

    class Meta:
        verbose_name = _('listing')
        verbose_name_plural = _('listings')
        ordering = ('title',)

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

    @property
    def get_price_display(self):
        if not self.price:
            return ''

        if inventor_settings.CURRENCY_AFTER_AMOUNT:
            price_display = '{}{}'.format(self.price, inventor_settings.CURRENCY)
        else:
            price_display = '{}{}'.format(inventor_settings.CURRENCY, self.price)

        if self.price_starts_at:
            price_display = '{} {}'.format(_('starts at'), price_display)

        if self.price_unit:
            price_display = '{} / {}'.format(price_display, self.get_price_unit_display())

        return price_display

    @cached_property
    def rating(self):
        avg_rating = self.comments.aggregate(Avg('rating'))
        rating = avg_rating['rating__avg']
        if rating:
            rating = round(rating, 2)
        return rating

    def delete(self, **kwargs):
        """ Deletes file before deleting instance """
        self.delete_banner()
        super().delete(**kwargs)

    def delete_banner(self):
        """ Deletes image file """
        try:
            os.remove(self.banner.path)
        except ValueError:
            pass
        except IOError:
            pass
        except OSError:
            pass


class Accommodation(BookingMixin, Listing):
    # TODO: type, class

    class Meta:
        verbose_name = _('accommodation')
        verbose_name_plural = _('accommodations')
        ordering = ('title',)


class Restaurant(Listing):
    class Meta:
        verbose_name = _('restaurant or bar')
        verbose_name_plural = _('restaurants and bars')
        ordering = ('title',)


class Business(Listing):
    class Meta:
        verbose_name = _('business')
        verbose_name_plural = _('businesses')
        ordering = ('title',)


class Travel(Listing):
    section = _('tourism')

    class Meta:
        verbose_name = _('travel')
        verbose_name_plural = _('travels')
        ordering = ('title',)


class Event(Listing):
    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
        ordering = ('title',)


class Shop(Listing):
    class Meta:
        verbose_name = _('shop')
        verbose_name_plural = _('shops')
        ordering = ('title',)


class Goods(Listing):
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


class Person(Listing):
    section = _('dating')

    class Meta:
        verbose_name = _('person')
        verbose_name_plural = _('persons')
        ordering = ('title',)


class Course(Listing):
    section = _('education')

    class Meta:
        verbose_name = _('course')
        verbose_name_plural = _('courses')
        ordering = ('title',)


class Animal(Listing):
    class Meta:
        verbose_name = _('animal')
        verbose_name_plural = _('animals')
        ordering = ('title',)


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

    def __str__(self):
        return self.title


class Amenity(models.Model):
    title = models.CharField(_('title'), max_length=100, unique=True)

    # TODO: listing types

    class Meta:
        verbose_name = _('amenity')
        verbose_name_plural = _('amenities')
        ordering = ('title',)

    def __str__(self):
        return self.title


class Feature(models.Model):
    title = models.CharField(_('title'), max_length=100, unique=True)

    # TODO: listing types

    class Meta:
        verbose_name = _('feature')
        verbose_name_plural = _('features')
        ordering = ('title',)

    def __str__(self):
        return self.title


class Location(models.Model):
    title = models.CharField(_('title'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name = _('location')
        verbose_name_plural = _('locations')
        ordering = ('title',)

    def __str__(self):
        return self.title


class Video(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=100, blank=True)
    description = models.TextField(_('description'), blank=True)
    url = models.URLField(_('URL'), max_length=300)

    class Meta:
        verbose_name = _('video')
        verbose_name_plural = _('video')
        ordering = ('title', )

    def __str__(self):
        return self.title if self.title else self.url


class Album(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name = _('album')
        verbose_name_plural = _('albums')
        ordering = ('title',)

    def __str__(self):
        return self.title


class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='as_photo')
    object_id = models.PositiveIntegerField()
    object = GenericForeignKey()
    file = models.ImageField(
        verbose_name=_('file'),
        help_text=_('photo, image or icon'),
        max_length=1024 * 5,
        upload_to='photos',
    )
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        verbose_name = _(u'photo')
        verbose_name_plural = _(u'photos')
        ordering = ('created',)

    def __unicode__(self):
        return self.file.name

    def delete(self, **kwargs):
        """ Deletes file before deleting instance """
        self.delete_file()
        super(Photo, self).delete(**kwargs)

    def delete_file(self):
        """ Deletes image file """
        try:
            os.remove(self.file.path)
        except ValueError:
            pass
        except IOError:
            pass
        except OSError:
            pass

    def get_absolute_url(self):
        return reverse('inventor:photo_download', kwargs={'pk': self.pk})
