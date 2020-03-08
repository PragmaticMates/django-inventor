from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from inventor.core.lexicons.models import Location, Category, Feature
from inventor.core.lexicons.models import AccommodationAmenity


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    search_fields = ['title']
    list_display = ('tree_actions', 'indented_title', 'slug', 'listing_type')
    list_display_links = ('indented_title',)
    list_select_related = ['listing_type']


@admin.register(Location)
class LocationAdmin(DraggableMPTTAdmin):
    search_fields = ['title']
    list_display = ('tree_actions', 'indented_title', 'slug')
    list_display_links = ('indented_title',)


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ('title', 'slug')


# Regular Lexicons

@admin.register(
    AccommodationAmenity,
    # AccommodationType, PropertyType
)
class RegularLexiconAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ('title', 'slug', 'description')
