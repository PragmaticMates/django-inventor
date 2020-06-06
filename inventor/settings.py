from django.conf import settings as django_settings

CURRENCY = getattr(django_settings, 'INVENTOR_CURRENCY', '€')
CURRENCY_AFTER_AMOUNT = getattr(django_settings, 'INVENTOR_CURRENCY_AFTER_AMOUNT', True)
PAGE_TITLE = getattr(django_settings, 'INVENTOR_PAGE_TITLE', 'Inventor')
PAGE_DESCRIPTION = getattr(django_settings, 'INVENTOR_PAGE_DESCRIPTION', 'Description')
PAGE_KEYWORDS = getattr(django_settings, 'INVENTOR_PAGE_KEYWORDS', 'Key words')
PAGE_APPLE_MOBILE_WEB_APP_TITLE = getattr(django_settings, 'INVENTOR_PAGE_APPLE_MOBILE_WEB_APP_TITLE', PAGE_TITLE)
LISTING_TYPES = getattr(django_settings, 'INVENTOR_LISTING_TYPES', None)
SECTIONS = getattr(django_settings, 'INVENTOR_SECTIONS', None)
VIDEOS_ENABLED = getattr(django_settings, 'INVENTOR_VIDEOS_ENABLED', True)
GALLERY_ENABLED = getattr(django_settings, 'INVENTOR_GALLERY_ENABLED', True)
