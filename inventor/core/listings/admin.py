from django.contrib import admin, messages
from django.contrib.admin.sites import NotRegistered
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from mapwidgets import GooglePointFieldWidget
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from sorl.thumbnail.admin import AdminImageMixin

from inventor import settings
from inventor.core.bookings.admin import BookingMixinAdmin
from inventor.core.listings.models.general import Album, Video, Photo, Listing
from inventor.core.listings.models.listing_types import Accommodation, Race
from inventor.core.utils.helpers import get_listing_types_classes


class PhotoInline(NestedStackedInline):
    model = Photo
    extra = 1


class AlbumInline(NestedStackedInline):
    model = Album
    extra = 1
    inlines = [PhotoInline]


class VideoInline(admin.StackedInline):
    model = Video
    extra = 1
    inlines = []


def make_convert_to_type_action(listing_type):
    def convert_to_type(modeladmin, request, queryset):
        for listing in queryset:
            listing.convert(listing_type)
            messages.info(request, "Listing {0} converted to {1}".format(listing, listing.get_listing_type_display()))

    listing_type_display = listing_type._meta.verbose_name
    convert_to_type.short_description = _("Convert to {0}").format(listing_type_display)
    # We need a different '__name__' for each action - Django
    # uses this as a key in the drop-down box.
    listing_type_identifier = listing_type.__name__.lower()
    convert_to_type.__name__ = 'convert_to_type_{0}'.format(listing_type_identifier)

    return convert_to_type


class ListingAdmin(AdminImageMixin, NestedModelAdmin):
    date_hierarchy = 'created'
    search_fields = ['id', 'title', 'description']
    list_display = ('id', 'title', 'slug', 'get_categories', 'address', 'locality', 'get_price_display', 'published', 'created')
    list_display_links = ('title',)
    list_filter = ('published', 'promoted')
    autocomplete_fields = ['author', 'locality']
    list_select_related = ['locality']
    filter_vertical = ['categories', 'features']  # TODO: filter categories for selected listing type only
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }

    class Media:
        js = (
            'js/map-widget-utils.js',
        )

    def get_actions(self, request):
        actions = super().get_actions(request)

        for listing_type in Listing.__subclasses__():
            action = make_convert_to_type_action(listing_type)
            actions[action.__name__] = (action,
                                        action.__name__,
                                        action.short_description)

        return actions

    def get_categories(self, obj):
        return ", ".join(obj.categories.values_list('title', flat=True))
    get_categories.admin_order_field = 'categories'
    get_categories.short_description = _('Categories')

    def get_price_display(self, obj):
        return obj.get_price_display()
    get_price_display.admin_order_field = 'price'
    get_price_display.short_description = _('Price')

    @property
    def fieldsets(self):
        fieldsets_definition = {
            'DEFINITION': (_('Definition'), {'fields': ('title', 'slug', 'description',)}),
            'MANAGEMENT': (_('Management'), {'fields': ('author', 'published', 'promoted')}),
            'SPECIFICATION': (_('Specification'), {'fields': (('categories', 'features'),)}),
            'PRICE': (_('Price'), {'fields': (('price_starts_at', 'price', 'price_unit', 'price_per_person'),)}),
            'LOCATION': (_('Location'), {'fields': ('locality', 'country', 'address', 'point')}),
            'PREVIEWS': (_('Previews'), {'fields': (('image', 'banner'),)}),
            'CONTACT': (_('Contact information'), {'fields': ('person', 'phone', 'email', 'website')}),
            'SOCIAL': (_('Social connections'), {'fields': ('social_networks',)}),
        }

        fieldsets = ()
        sections = settings.SECTIONS or fieldsets_definition.keys()

        for section in sections:
            fieldsets += fieldsets_definition[section],

        return fieldsets

    @property
    def inlines(self):
        inlines = []
        if settings.VIDEOS_ENABLED:
            inlines.append(VideoInline)
        if settings.GALLERY_ENABLED:
            inlines.append(AlbumInline)
        # add comments?
        return inlines


class PhotoInline(admin.StackedInline):
    model = Photo
    extra = 1


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    search_fields = ['listing__title', 'title', 'description']
    list_display = ('listing', 'title', 'description')
    raw_id_fields = ['listing']
    inlines = [PhotoInline]


# Listing types
@admin.register(*get_listing_types_classes())
class ListingTypeAdmin(ListingAdmin):
    pass


try:
    admin.site.unregister(Accommodation)
    @admin.register(Accommodation)
    class AccommodationAdmin(ListingAdmin):
        fieldsets = ListingTypeAdmin.fieldsets + BookingMixinAdmin.fieldsets + (
            (_('Specific'), {'fields': ('amenities', 'star_rating', 'rooms')}),
        )
except (NotRegistered, TypeError):
    pass


try:
    admin.site.unregister(Race)
    @admin.register(Race)
    class RaceAdmin(ListingAdmin):
        list_display = ListingTypeAdmin.list_display + ('distance_display',)
        list_filter = ListingTypeAdmin.list_filter + ('distance', )

        def distance_display(self, obj):
            return obj.get_distance_display()
        distance_display.admin_order_field = 'distance'
        distance_display.short_description = _('Distance')

        @property
        def fieldsets(self):
            return super().fieldsets + (
                (_('Specific'), {'fields': ('distance',)}),
            )
except NotRegistered:
    pass
