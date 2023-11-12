from django.db import models
from django.utils.translation import gettext_lazy as _


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed = models.DateTimeField(_(u'subscribed'), auto_now_add=True)

    class Meta:
        verbose_name = _(u'subscriber')
        verbose_name_plural = _(u'subscribers')
        ordering = ['email']

    def __str__(self):
        return self.email
