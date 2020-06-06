from django.utils.module_loading import import_string

from inventor import settings


def get_listing_types_classes():
    listing_types = settings.LISTING_TYPES
    from inventor.core.listings.models.general import Listing

    if listing_types is None:
        subclasses = Listing.__subclasses__()
        return subclasses

    listing_types_classes = []
    for listing_type in listing_types:
        listing_type_class = import_string(f'inventor.core.listings.models.listing_types.{listing_type}')
        listing_types_classes.append(listing_type_class)

    return listing_types_classes
