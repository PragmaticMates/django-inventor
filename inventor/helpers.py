from django.utils.module_loading import import_string

from inventor import settings


def get_listing_types_classes():
    from inventor.core.listings.models.general import Listing
    listing_types = settings.LISTING_TYPES

    if listing_types is None:
        subclasses = Listing.__subclasses__()
        return subclasses

    listing_types_classes = []
    for listing_type in listing_types:
        listing_type_class = import_string(f'inventor.core.listings.models.listing_types.{listing_type}')
        listing_types_classes.append(listing_type_class)

    return listing_types_classes


def is_listing_type_enabled(listing_type_str):
    listing_types = settings.LISTING_TYPES
    return True if listing_types is None else listing_type_str in listing_types
