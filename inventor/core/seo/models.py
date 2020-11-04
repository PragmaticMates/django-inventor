from django.contrib.postgres.indexes import GinIndex
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from modeltrans.fields import TranslationField

from inventor.core.seo.querysets import SeoQuerySet


class Seo(models.Model):
    ROBOTS = [
        ('index', 'index'),
        ('noindex', 'noindex'),
        ('follow', 'follow'),
        ('noindex, follow', 'noindex, follow'),
        ('index, nofollow', 'index, nofollow'),
        ('noindex, nofollow', 'noindex, nofollow'),
    ]

    title = models.CharField(verbose_name=_('title'), max_length=200, default='', blank=True)
    description = models.CharField(verbose_name=_('description'), max_length=200, default='', blank=True)
    keywords = models.CharField(verbose_name=_('keywords'), max_length=1000, default='', blank=True)
    robots = models.CharField(verbose_name=_('robots'), choices=ROBOTS, max_length=17, blank=True, default='',
        help_text=_('Default (empty) = index, follow'))
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    objects = SeoQuerySet.as_manager()
    i18n = TranslationField(fields=('title', 'description', 'keywords'))

    class Meta:
        verbose_name = _('SEO fields')
        verbose_name_plural = _('SEO fields')
        unique_together = ('content_type', 'object_id')
        indexes = [GinIndex(fields=["i18n"]), ]

    def __str__(self):
        return self.title_i18n
