from django.conf import settings as django_settings


CURRENCY = getattr(django_settings, 'INVENTOR_CURRENCY', '€')
CURRENCY_AFTER_AMOUNT = getattr(django_settings, 'INVENTOR_CURRENCY_AFTER_AMOUNT', True)
