from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from inventor.core.listings.mixins import SlugMixin


class Category(SlugMixin, MPTTModel):
    title = models.CharField(_('title'), max_length=100, unique=True)
    slug = models.SlugField(unique=True, max_length=SlugMixin.MAX_SLUG_LENGTH, default='')
    listing_type = models.ForeignKey(
        ContentType, verbose_name=_('listing type'), on_delete=models.PROTECT,
        blank=True, null=True, default=None)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('title',)

    def __str__(self):
        return self.title


class Feature(SlugMixin, models.Model):
    title = models.CharField(_('title'), max_length=100, unique=True)
    slug = models.SlugField(unique=True, max_length=SlugMixin.MAX_SLUG_LENGTH, default='')
    # listing_type = models.ForeignKey(
    #     ContentType, verbose_name=_('listing type'), on_delete=models.PROTECT,
    #     blank=True, null=True, default=None)

    class Meta:
        verbose_name = _('feature')
        verbose_name_plural = _('features')
        ordering = ('title',)

    def __str__(self):
        return self.title


class Location(SlugMixin, MPTTModel):
    title = models.CharField(_('title'), max_length=100, unique=True)
    slug = models.SlugField(unique=True, max_length=SlugMixin.MAX_SLUG_LENGTH, default='')
    description = models.TextField(_('description'), blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = _('location')
        verbose_name_plural = _('locations')
        ordering = ('title',)

    def __str__(self):
        return self.title
