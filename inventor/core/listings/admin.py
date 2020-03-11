from django.contrib import admin, messages
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from mapwidgets import GooglePointFieldWidget
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from sorl.thumbnail.admin import AdminImageMixin

from inventor.core.bookings.admin import BookingMixinAdmin
from inventor.core.listings.models.general import Album, Video, Photo, Listing
from inventor.core.listings.models.listing_types import Accommodation, Property, EatAndDrink, Service, Vacation, Event, Shop, Vehicle, Profile, Job, Course, \
    Nature


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
    list_display = ('id', 'title', 'slug', 'address', 'location', 'created')
    list_display_links = ('title',)
    # list_filter = ('location', 'country', )
    autocomplete_fields = ['author', 'location']
    list_select_related = ['location']
    inlines = [VideoInline, AlbumInline]  # add comments?

    fieldsets = (
        (_('Definition'), {'fields': ('title', 'slug', 'description',)}),
        (_('Management'), {'fields': ('author', 'published', 'promoted')}),
        (_('Specification'), {'fields': (('categories', 'features'),)}),
        (_('Price'), {'fields': (('price_starts_at', 'price', 'price_unit', 'price_per_person'),)}),
        (_('Address'), {'fields': ('location', 'country', 'address', 'point')}),
        (_('Previews'), {'fields': (('image', 'banner'),)}),
        (_('Contact information'), {'fields': ('person', 'phone', 'email', 'website')}),
        (_('Social connections'), {'fields': ('social_networks',)}),
    )
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

@admin.register(*Listing.__subclasses__())
class ListingTypeAdmin(ListingAdmin):
    pass

admin.site.unregister(Accommodation)
@admin.register(Accommodation)
class AccommodationAdmin(ListingAdmin):
    fieldsets = ListingTypeAdmin.fieldsets + BookingMixinAdmin.fieldsets + (
        (_('Specific'), {'fields': ('amenities', 'star_rating', 'rooms')}),
    )
