from django.contrib import admin
from inventor.core.partners.models import Partner


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title', 'image', 'is_main', 'website', 'description')
    list_filter = ['is_main']
    readonly_fields = ('created', 'modified')
