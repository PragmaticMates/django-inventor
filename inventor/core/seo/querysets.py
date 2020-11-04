from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class SeoQuerySet(models.QuerySet):
    def for_subject(self, subject):
        return self.filter(path_i18n=subject).first() if isinstance(subject, str) else self.for_object(subject)

    def for_path(self, path):
        return self.filter(path_i18n=path)

    def for_object(self, instance):
        try:
            ct = ContentType.objects.get_for_model(instance.__class__)
        except AttributeError:
            return None

        try:
            return self.filter(content_type=ct).get(object_id=instance.id)
        except ObjectDoesNotExist:
            return None
