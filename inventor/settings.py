from django.conf import settings as django_settings

CURRENCY = getattr(django_settings, 'INVENTOR_CURRENCY', 'EUR')
CURRENCY_SYMBOL = getattr(django_settings, 'INVENTOR_CURRENCY_SYMBOL', '€')
CURRENCY_AFTER_AMOUNT = getattr(django_settings, 'INVENTOR_CURRENCY_AFTER_AMOUNT', True)
PAGE_TITLE = getattr(django_settings, 'INVENTOR_PAGE_TITLE', 'Inventor')
PAGE_DESCRIPTION = getattr(django_settings, 'INVENTOR_PAGE_DESCRIPTION', 'Description')
PAGE_KEYWORDS = getattr(django_settings, 'INVENTOR_PAGE_KEYWORDS', 'Key words')
PAGE_APPLE_MOBILE_WEB_APP_TITLE = getattr(django_settings, 'INVENTOR_PAGE_APPLE_MOBILE_WEB_APP_TITLE', PAGE_TITLE)
LISTING_TYPES = getattr(django_settings, 'INVENTOR_LISTING_TYPES', None)
SECTIONS = getattr(django_settings, 'INVENTOR_SECTIONS', None)
VIDEOS_ENABLED = getattr(django_settings, 'INVENTOR_VIDEOS_ENABLED', True)
GALLERY_ENABLED = getattr(django_settings, 'INVENTOR_GALLERY_ENABLED', True)
LISTING_FILTER = getattr(django_settings, 'INVENTOR_LISTING_FILTER', {})
USER_FORM_COLUMNS = getattr(django_settings, 'INVENTOR_USER_FORM_COLUMNS', True)
USER_REQUIRED_FIELDS = getattr(django_settings, 'INVENTOR_USER_REQUIRED_FIELDS', [])
USER_HIDDEN_FIELDS = getattr(django_settings, 'INVENTOR_USER_HIDDEN_FIELDS', [])
USE_PLACEHOLDERS = getattr(django_settings, 'INVENTOR_USE_PLACEHOLDERS', False)
LISTINGS_URL_ENABLED = getattr(django_settings, 'INVENTOR_LISTINGS_URL_ENABLED', True)
SEO_FOR_MODELS = getattr(django_settings, 'INVENTOR_SEO_FOR_MODELS', ['Listing'])
LISTING_SORTING_OPTIONS = getattr(django_settings, 'INVENTOR_LISTING_SORTING_OPTIONS', {
    '-promoted': ['-promoted', 'awaiting', '-created']
})
