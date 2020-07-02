import os
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from sorl import thumbnail


class Partner(models.Model):
    title = models.CharField(_('title'), max_length=100)
    image = thumbnail.ImageField(
        verbose_name=_('image'),
        help_text=_('logo or image'),
        max_length=1024,
        upload_to='images',
        blank=True
    )
    website = models.URLField(_('website'), help_text='URL', blank=True)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        verbose_name = _('partner')
        verbose_name_plural = _('partners')
        ordering = ('title',)

    def __str__(self):
        return self.title

    def delete(self, **kwargs):
        """ Deletes file before deleting instance """
        self.delete_image()
        super().delete(**kwargs)

    def delete_image(self):
        """ Deletes image file """
        try:
            os.remove(self.image.path)
        except ValueError:
            pass
        except IOError:
            pass
        except OSError:
            pass
