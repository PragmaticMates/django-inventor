from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from mptt.admin import DraggableMPTTAdmin
from sorl.thumbnail.admin import AdminImageMixin
from inventor.core.lexicons.models import Locality, Category, Feature
from inventor.core.utils.helpers import get_listing_types_classes, is_listing_type_enabled


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    search_fields = ['title']
    list_display = ('tree_actions', 'title_i18n', 'slug_i18n', 'listing_type', 'icon', 'color_display')
    list_display_links = ('title_i18n',)
    list_editable = ['icon']
    list_select_related = ['listing_type']

    def color_display(self, obj):
        return mark_safe(f'<span style="background-color:{obj.color};width:15px;height:15px;display:inline-block;vertical-align:-3px;"></span> {obj.color}')
    color_display.admin_order_field = 'color'
    color_display.short_description = _('Color')


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

# from inventor.core.listings.models.listing_types import Accommodation
# if Accommodation in get_listing_types_classes():
if is_listing_type_enabled('Accommodation'):
    from inventor.core.lexicons.models import AccommodationAmenity
    regular_lexicons.append(AccommodationAmenity)

if len(regular_lexicons) > 0:
    @admin.register(
        *regular_lexicons,
        # AccommodationType, PropertyType
    )
    class RegularLexiconAdmin(admin.ModelAdmin):
        search_fields = ['title']
        list_display = ('title', 'slug', 'description')
