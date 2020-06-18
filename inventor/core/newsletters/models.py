from django.db import models
from django.utils.translation import ugettext_lazy as _


class Subscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed = models.DateTimeField(_(u'subscribed'), auto_now_add=True)

    class Meta:
        verbose_name = _(u'subscription')
        verbose_name_plural = _(u'subscriptions')
        ordering = ['email']

    def __str__(self):
        return self.email
