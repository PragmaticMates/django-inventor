import os
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import HStoreField
from django.contrib.gis.db import models
from django.contrib.gis.db.models import Avg
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django_comments import get_model as get_comment_model
from internationalflavor.countries import CountryField
from sorl import thumbnail

from inventor import settings as inventor_settings
from inventor.core.lexicons.models import Category, Feature, Location
from inventor.core.listings.managers import ListingQuerySet


# TODO: opening hours, meals and drinks, street view, faq
from inventor.core.listings.mixins import SlugMixin


class Listing(SlugMixin, models.Model):
    FORCE_SLUG_REGENERATION = False

    SOCIAL_NETWORKS = ['Facebook', 'Twitter', 'Google', 'Instagram', 'Vimeo', 'YouTube', 'LinkedIn', 'Dribbble',
                       'Skype', 'Foursquare', 'Behance']  # TODO: move to settings

    PRICE_UNITS = [
        ('ENTRY', _('entry')),                    # tickets
        ('HOUR', _('hour')),                      # parking
        ('DAY', _('day')),                        # vehicle per day
        ('NIGHT', _('night')),                    # room unit per night
    ]

    # definition
    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(unique=True, max_length=SlugMixin.MAX_SLUG_LENGTH)
    description = models.TextField(_('description'), blank=True)

    # management
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('author'))
    published = models.BooleanField(_('published'), default=True)
    promoted = models.BooleanField(_('promoted'), default=False)

    # specification
    categories = models.ManyToManyField(to=Category, verbose_name=_('categories'), blank=True, related_name='listings_of_category')
    features = models.ManyToManyField(to=Feature, verbose_name=_('features'), blank=True, related_name='listings_with_features')

    # price
    price_starts_at = models.BooleanField(_('price starts at'), default=False)
    price = models.DecimalField(_('price'), help_text=inventor_settings.CURRENCY, max_digits=10, decimal_places=2, db_index=True, validators=[MinValueValidator(0)],
                                blank=True, null=True, default=None)
    price_unit = models.CharField(_('price unit'), choices=PRICE_UNITS, max_length=5, blank=True)
    price_per_person = models.BooleanField(_('price per person'), default=False)

    # address
    location = models.ForeignKey(Location, on_delete=models.SET_NULL,
                                 blank=True, null=True, default=None)

    address = models.TextField(_('address'), help_text=_('street, postcode, city'), max_length=500, blank=True)

    # street = models.CharField(_('street'), max_length=200, blank=True)
    # postcode = models.CharField(_('postcode'), max_length=30, blank=True)
    # city = models.CharField(_('city'), max_length=50, blank=True)
    country = CountryField(verbose_name=_('country'), blank=True, db_index=True)
    point = models.PointField(_('point'), blank=True, null=True, default=None, db_index=True)

    # previews
    image = thumbnail.ImageField(
        verbose_name=_('image'),
        help_text=_('photo or image'),
        max_length=1024,
        upload_to='images',
        blank=True
    )

    banner = models.ImageField(
        verbose_name=_('banner'),
        help_text=_('photo or image'),
        max_length=1024 * 5,
        upload_to='banners',
        blank=True
    )

    # contact information
    person = models.CharField(_('person'), max_length=100, blank=True)
    phone = models.CharField(_('phone'), max_length=40, blank=True)
    email = models.EmailField(_('email'), blank=True)
    website = models.URLField(_('website'), max_length=400, blank=True)

    # social
    social_networks = HStoreField(verbose_name=_('social networks'), blank=True, default=dict)

    # relations
    comments = GenericRelation(get_comment_model(), content_type_field='content_type', object_id_field='object_pk',
                               related_query_name='comment')

    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    objects = ListingQuerySet.as_manager()

    class Meta:
        verbose_name = _('listing')
        verbose_name_plural = _('listings')
        ordering = ('title',)
        db_table = 'listings_general'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('listings:listing_detail', args=(self.slug,))

    def get_update_url(self):
        return reverse('listings:listing_update', args=(self.pk,))

    @property
    def full_address(self):
        return '{}, {}'.format(self.address, self.country).strip(', ')

    @property
    def get_price_display(self):
        if not self.price:
            return ''

        price = str(self.price)

        if price.endswith('.00'):
            price = price[:-3]

        if inventor_settings.CURRENCY_AFTER_AMOUNT:
            price_display = '{}{}'.format(price, inventor_settings.CURRENCY)
        else:
            price_display = '{}{}'.format(inventor_settings.CURRENCY, price)

        if self.price_starts_at:
            price_display = '{} {}'.format(_('starts at'), price_display)

        if self.price_unit:
            price_display = '{} / {}'.format(price_display, self.get_price_unit_display())

        return price_display

    @cached_property
    def rating(self):
        avg_rating = self.comments.aggregate(Avg('rating'))
        # TODO: rating subjects:
        # - Facilities / Amenities
        # - Cleanliness
        # - Comfort
        # - Location
        # - Services?
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

    @property
    def listing_class(self):
        return self.__class__

    def get_listing_type_display(self):
        return self.listing_class._meta.verbose_name

    def get_listing_type_display_plural(self):
        return self.listing_class._meta.verbose_name_plural

    @classmethod
    def get_list_url_name(cls):
        url_name = f'{cls.__name__.lower()}_list'
        return f'{url_name}'

    @classmethod
    def get_list_url(cls):
        url_name = cls.get_list_url_name()
        return reverse(f'listings:{url_name}')

    def get_real_instance(self):
        """ get object child instance """

        def get_subclasses(cls):
            subclasses = cls.__subclasses__()
            result = []
            for subclass in subclasses:
                if not subclass._meta.abstract:
                    result.append(subclass)
                else:
                    result += get_subclasses(subclass)
            return result

        if hasattr(self, '_real_instance'):  # try looking in our cache
            return self._real_instance

        subclasses = get_subclasses(self.__class__)

        if not subclasses:  # already real_instance
            self._real_instance = self
            return self._real_instance
        else:
            subclasses_names = [cls.__name__.lower() for cls in subclasses]
            for subcls_name in subclasses_names:
                if hasattr(self, subcls_name):
                    return getattr(self, subcls_name, self)
            return self


class Video(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=100, blank=True)
    description = models.TextField(_('description'), blank=True)
    url = models.URLField(_('URL'), max_length=300)

    class Meta:
        verbose_name = _('video')
        verbose_name_plural = _('videos')
        ordering = ('title', )

    def __str__(self):
        return self.title if self.title else self.url


class Album(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=100, blank=True)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        verbose_name = _('album')
        verbose_name_plural = _('albums')
        ordering = ('title',)

    def __str__(self):
        return self.title


class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    file = models.ImageField(
        verbose_name=_('file'),
        help_text=_('photo, image or icon'),
        max_length=1024 * 5,
        upload_to='photos',  # TODO: listing folder
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
