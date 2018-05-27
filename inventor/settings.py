from django.conf import settings as django_settings


CURRENCY = getattr(django_settings, 'INVENTOR_CURRENCY', '€')
