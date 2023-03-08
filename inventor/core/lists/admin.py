from django.contrib import admin
from django.utils.safestring import mark_safe

from inventor.core.lists.models import List


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    search_fields = ['title', 'user__first_name', 'user__last_name']
    list_display = ('title', 'user', 'list_of_listings')
    # autocomplete_fields = ['listings']  # An admin for model "Listing" has to be registered
    autocomplete_fields = ['user']
    filter_horizontal = ['listings']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('listings')

    def list_of_listings(self, obj):
        return mark_safe('<br>'.join(map(str, obj.listings.all())))
