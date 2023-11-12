from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from inventor.core.listings.models.general import Listing


class List(models.Model):
    user = models.ForeignKey(get_user_model(), verbose_name=_('user'), on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    listings = models.ManyToManyField(to=Listing, verbose_name=_('listings'), blank=True, related_name='lists')

    class Meta:
        verbose_name = _('list')
        verbose_name_plural = _('lists')
        ordering = ('title',)
        unique_together = [('user', 'title'),]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('inventor:lists:list_detail', args=(self.id,))
