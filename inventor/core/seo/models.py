from django.contrib.postgres.indexes import GinIndex
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from modeltrans.fields import TranslationField
from sorl import thumbnail

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

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True, default=None)
    object_id = models.PositiveIntegerField(blank=True, null=True, default=None)
    content_object = GenericForeignKey('content_type', 'object_id')
    path = models.CharField(verbose_name=_('request path'), max_length=100, blank=True, default='')

    title = models.CharField(verbose_name=_('title'), max_length=200)
    description = models.CharField(verbose_name=_('description'), max_length=200)
    keywords = models.CharField(verbose_name=_('keywords'), max_length=1000)
    robots = models.CharField(verbose_name=_('robots'), choices=ROBOTS, max_length=17, blank=True, default='',
        help_text=_('Default (empty) = index, follow'))
    image = thumbnail.ImageField(
        verbose_name=_('image'),
        help_text=_('Min resolution: 200 x 200 px. Suggested resolution: 1200 x 630 px (1.9:1). <a href="https://developers.facebook.com/docs/sharing/webmasters/images/" target="_blank">Read more</a>.'),
        max_length=8*1024,
        upload_to='images',
        blank=True
    )
    objects = SeoQuerySet.as_manager()
    i18n = TranslationField(fields=('title', 'description', 'keywords', 'path'))

    class Meta:
        verbose_name = _('SEO fields')
        verbose_name_plural = _('SEO fields')
        unique_together = ('content_type', 'object_id', 'path')
        indexes = [GinIndex(fields=["i18n"]), ]

    def __str__(self):
        return self.title_i18n
