from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from inventor.core.lexicons.models import Location, Category, Feature


@admin.register(Category, Location)
class CategoryAndLocationAdmin(DraggableMPTTAdmin):
    search_fields = ['title']
    list_display = ('tree_actions', 'indented_title', 'slug')
    list_display_links = ('indented_title',)


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ('title', 'slug')
