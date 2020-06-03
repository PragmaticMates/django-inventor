import os

from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db import models
from django.contrib.postgres.indexes import GinIndex
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from modeltrans.fields import TranslationField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from sorl import thumbnail
from inventor.core.listings.mixins import SlugMixin
from inventor.core.lexicons.querysets import CategoryManager


class RegularLexicon(SlugMixin, models.Model):
    title = models.CharField(_('title'), max_length=100, unique=True)
    slug = models.SlugField(unique=True, max_length=SlugMixin.MAX_SLUG_LENGTH, default='')
    description = models.TextField(_('description'), blank=True)

    class Meta:
        abstract = True
        ordering = ('title',)

    def __str__(self):
        return self.title


class Category(SlugMixin, MPTTModel):
    title = models.CharField(_('title'), max_length=100)
    slug = models.SlugField(unique=True, max_length=SlugMixin.MAX_SLUG_LENGTH, default='')
    listing_type = models.ForeignKey(
        ContentType, verbose_name=_('listing type'), on_delete=models.SET_NULL,
        blank=True, null=True, default=None)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    i18n = TranslationField(fields=('title', 'slug'))
    objects = CategoryManager()

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('title',)
        unique_together = (('title', 'listing_type'),)
        indexes = [GinIndex(fields=["i18n"]), ]

    def __str__(self):
        return self.title_i18n


class Feature(SlugMixin, models.Model):
    title = models.CharField(_('title'), max_length=100, unique=True)
    slug = models.SlugField(unique=True, max_length=SlugMixin.MAX_SLUG_LENGTH, default='')
    # listing_type = models.ForeignKey(
    #     ContentType, verbose_name=_('listing type'), on_delete=models.PROTECT,
    #     blank=True, null=True, default=None)  # or many to many?

    class Meta:
        verbose_name = _('feature')
        verbose_name_plural = _('features')
        ordering = ('title',)

    def __str__(self):
        return self.title


class Locality(SlugMixin, MPTTModel):
    title = models.CharField(_('title'), max_length=100, unique=True)
    slug = models.SlugField(unique=True, max_length=SlugMixin.MAX_SLUG_LENGTH, default='')
    description = models.TextField(_('description'), blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    photo = thumbnail.ImageField(
        verbose_name=_('photo'),
        max_length=1024 * 5,
        upload_to='localities',
        blank=True, null=True, default=None
    )

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = _('locality')
        verbose_name_plural = _('localities')
        ordering = ('title',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from inventor.core.listings.models.general import Listing
        url = Listing.get_list_url()
        return f'{url}?locality={self.slug}'

    def delete(self, **kwargs):
        """ Deletes file before deleting instance """
        self.delete_file()
        super().delete(**kwargs)

    def delete_file(self):
        """ Deletes image file """
        try:
            os.remove(self.photo.path)
        except ValueError:
            pass
        except IOError:
            pass
        except OSError:
            pass


# Accommodation

class AccommodationAmenity(RegularLexicon):
    class Meta:
        verbose_name = _('accommodation amenity')
        verbose_name_plural = _('accommodation amenities')
        ordering = ('title',)


# TODO: Deprecated: replaced by categories

# class AccommodationType(RegularLexicon):
#     class Meta:
#         verbose_name = _('accommodation type')
#         verbose_name_plural = _('accommodation types')
#         ordering = ('title',)


# Property

# TODO: Deprecated: replaced by categories
# class PropertyType(RegularLexicon):
#     class Meta:
#         verbose_name = _('property type')
#         verbose_name_plural = _('property types')
#         ordering = ('title',)


from .signals import *  # TODO: move to AppConfig
