from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from sorl.thumbnail.admin import AdminImageMixin
from inventor.core.lexicons.models import Locality, Category, Feature
from inventor.core.lexicons.models import AccommodationAmenity
from inventor.core.listings.models.listing_types import Accommodation
from inventor.core.utils.helpers import get_listing_types_classes


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    search_fields = ['title']
    list_display = ('tree_actions', 'title_i18n', 'slug_i18n', 'listing_type')
    list_display_links = ('title_i18n',)
    list_select_related = ['listing_type']


@admin.register(Locality)
class LocalityAdmin(AdminImageMixin, DraggableMPTTAdmin):
    search_fields = ['title']
    list_display = ('tree_actions', 'indented_title', 'slug')
    list_display_links = ('indented_title',)


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ('title', 'slug')


# Regular Lexicons
regular_lexicons = []
if Accommodation in get_listing_types_classes():
    regular_lexicons.append(AccommodationAmenity)

if len(regular_lexicons) > 0:
    @admin.register(
        *regular_lexicons,
        # AccommodationType, PropertyType
    )
    class RegularLexiconAdmin(admin.ModelAdmin):
        search_fields = ['title']
        list_display = ('title', 'slug', 'description')
