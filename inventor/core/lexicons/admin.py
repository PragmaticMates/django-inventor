from django.contrib import admin
from django.db import models
from django.forms import TextInput
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from modeltrans.admin import ActiveLanguageMixin
from mptt.admin import DraggableMPTTAdmin, TreeRelatedFieldListFilter
from sorl.thumbnail.admin import AdminImageMixin
from inventor.core.lexicons.models import Locality, Category, Feature
from inventor.helpers import get_listing_types_classes


@admin.register(Category)
class CategoryAdmin(ActiveLanguageMixin, DraggableMPTTAdmin):
    search_fields = ['title_i18n']
    actions = ['rebuild']
    list_display = ('tree_actions', 'indented_title_i18n', 'slug_i18n', 'description_i18n', 'listing_type', 'icon', 'color_display')
    list_display_links = ('indented_title_i18n',)
    list_editable = ['icon', 'description_i18n']
    list_select_related = ['listing_type']
    formfield_overrides = {
        models.TextField: {'widget': TextInput(attrs={'class': 'vTextField'})},
    }

    def rebuild(self, request, queryset):
        Category.objects.rebuild()

    def indented_title_i18n(self, instance):
        return format_html(
            '<div style="text-indent:{}px">{}</div>',
            instance._mpttfield('level') * self.mptt_level_indent,
            instance.title_i18n,
        )
    indented_title_i18n.short_description = _('Title')

    def color_display(self, obj):
        return mark_safe(f'<span style="background-color:{obj.color};width:15px;height:15px;display:inline-block;vertical-align:-3px;"></span> {obj.color}')
    color_display.admin_order_field = 'color'
    color_display.short_description = _('Color')


@admin.register(Locality)
class LocalityAdmin(ActiveLanguageMixin, AdminImageMixin, DraggableMPTTAdmin):
    search_fields = ['title_i18n']
    list_display = ('tree_actions', 'indented_title', 'slug', 'description_i18n')
    list_display_links = ('indented_title',)


@admin.register(Feature)
class FeatureAdmin(ActiveLanguageMixin, admin.ModelAdmin):
    search_fields = ['title_i18n']
    list_display = ('title_i18n', 'slug_i18n')


# Regular Lexicons
regular_lexicons = []

from inventor.core.listings.models.listing_types import Accommodation
if Accommodation in get_listing_types_classes():
    from inventor.core.lexicons.models import AccommodationAmenity
    regular_lexicons.append(AccommodationAmenity)

if len(regular_lexicons) > 0:
    @admin.register(
        *regular_lexicons,
        # AccommodationType, PropertyType
    )
    class RegularLexiconAdmin(ActiveLanguageMixin, admin.ModelAdmin):
        search_fields = ['title_i18n']
        list_display = ('title_i18n', 'description_i18n', 'slug', 'description')
