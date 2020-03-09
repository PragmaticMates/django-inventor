from django.contrib import admin
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from mapwidgets import GooglePointFieldWidget
from sorl.thumbnail.admin import AdminImageMixin

from inventor.core.bookings.admin import BookingMixinAdmin
from inventor.core.listings.models.general import Album, Video, Photo
from inventor.core.listings.models.listing_types import Accommodation, Property, EatAndDrink, Service, Vacation, Event, Shop, Vehicle, Profile, Job, Course, \
    Nature


class AlbumInline(admin.StackedInline):
    model = Album
    extra = 1


class VideoInline(admin.StackedInline):
    model = Video
    extra = 1


class ListingAdmin(AdminImageMixin, admin.ModelAdmin):
    date_hierarchy = 'created'
    search_fields = ['title', 'description']
    list_display = ('id', 'title', 'slug', 'address', 'location', 'created')
    list_display_links = ('title',)
    # list_filter = ('location', 'country', )
    autocomplete_fields = ['author', 'location']

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
    inlines = [VideoInline, AlbumInline]  # add comments?
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }

    class Media:
        js = (
            'js/map-widget-utils.js',
        )


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

@admin.register(Property, EatAndDrink, Service, Vacation, Event, Shop, Vehicle, Profile, Job, Course, Nature)
class ListingTypeAdmin(ListingAdmin):
    pass


@admin.register(Accommodation)
class AccommodationAdmin(ListingAdmin):
    fieldsets = ListingTypeAdmin.fieldsets + BookingMixinAdmin.fieldsets + (
        (_('Specific'), {'fields': ('amenities', 'star_rating', 'rooms')}),
    )
