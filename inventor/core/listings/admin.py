from django.contrib import admin
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from mapwidgets import GooglePointFieldWidget
from mptt.admin import DraggableMPTTAdmin

from inventor.core.listings.models.general import Album, Location, Category, Feature, Video, Photo
from inventor.core.listings.models.listing_types import Accommodation, Property, EatAndDrink, Service, Vacation, Event, Goods, Vehicle, Profile, Job, Course, \
    Nature  # TODO: add remaining types


class AlbumInline(admin.StackedInline):
    model = Album
    extra = 1


class VideoInline(admin.StackedInline):
    model = Video
    extra = 1


class ListingAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    search_fields = ['title', 'description']
    list_display = ('id', 'title', 'address', 'location', 'created')
    list_filter = ('country', )
    autocomplete_fields = ['author', 'location']
    fieldsets = (
        (_('Definition'), {'fields': ('title', 'description',)}),
        (_('Management'), {'fields': ('author', 'published', 'promoted')}),
        (_('Specification'), {'fields': (('categories', 'features'),)}),
        (_('Price'), {'fields': (('price_starts_at', 'price', 'price_unit'),)}),
        (_('Address'), {'fields': ('location', 'street', 'postcode', 'city', 'country', 'point')}),
        (_('Previews'), {'fields': (('image', 'banner'),)}),
        (_('Contact information'), {'fields': ('person', 'phone', 'email', 'website')}),
        (_('Social connections'), {'fields': ('social_networks',)}),
    )
    filter_vertical = ['categories', 'features']
    inlines = [VideoInline, AlbumInline]  # add comments?
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }

    class Media:
        js = (
            'js/map-widget-utils.js',
        )


@admin.register(Category, Location)
class CategoryAndLocationAdmin(DraggableMPTTAdmin):
    search_fields = ['title']
    list_display = ('tree_actions', 'indented_title')
    list_display_links = ('indented_title', )


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ('title',)


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

@admin.register(Property, Accommodation, EatAndDrink, Service, Vacation, Event, Goods, Vehicle, Profile, Job, Course, Nature)
class ListingTypeAdmin(ListingAdmin):
    pass
