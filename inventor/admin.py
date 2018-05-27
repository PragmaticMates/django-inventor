from django.contrib import admin
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from mapwidgets import GooglePointFieldWidget
from inventor.models import Album, Accommodation, Location


class AlbumInline(admin.StackedInline):
    model = Album
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
        (_('Specification'), {'fields': (('categories', 'amenities', 'features'),)}),
        (_('Price'), {'fields': (('price_starts_at', 'price', 'price_unit'),)}),
        (_('Address'), {'fields': ('location', 'street', 'postcode', 'city', 'country', 'point')}),
        (_('Previews'), {'fields': (('image', 'banner'),)}),
        (_('Contact information'), {'fields': ('person', 'phone', 'email', 'website')}),
        (_('Social connections'), {'fields': ('social_networks',)}),
    )
    inlines = [AlbumInline]  # add comments?
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }

    class Media:
        js = (
            'js/map-widget-utils.js',
        )


@admin.register(Accommodation)
class AccommodationAdmin(ListingAdmin):
    pass


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    search_fields = ['title', 'description']
    list_display = ('title', 'description')
