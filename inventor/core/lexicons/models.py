from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    title = models.CharField(_('title'), max_length=100, unique=True)
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


class Feature(models.Model):
    # WiFi, TV, hairdryer
    # pet friendly, free parking, wheelchair accessible
    title = models.CharField(_('title'), max_length=100, unique=True)
    listing_type = models.ForeignKey(
        ContentType, verbose_name=_('listing type'), on_delete=models.PROTECT,
        blank=True, null=True, default=None)

    class Meta:
        verbose_name = _('feature')
        verbose_name_plural = _('features')
        ordering = ('title',)

    def __str__(self):
        return self.title


class Location(MPTTModel):
    title = models.CharField(_('title'), max_length=100, unique=True)
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
