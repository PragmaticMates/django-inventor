from django.contrib.gis.db import models
from django.contrib.postgres.indexes import GinIndex
from django.utils.translation import ugettext_lazy as _
from modeltrans.fields import TranslationField


class FAQ(models.Model):
    question = models.CharField(_('question'), max_length=200, blank=False)
    answer = models.TextField(_('answer'), blank=False)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    i18n = TranslationField(fields=('question', 'answer'))

    class Meta:
        verbose_name = _('frequently asked question')
        verbose_name_plural = _('frequently asked questions')
        ordering = ('question',)
        indexes = [GinIndex(fields=["i18n"]), ]

    def __str__(self):
        return self.question_i18n
