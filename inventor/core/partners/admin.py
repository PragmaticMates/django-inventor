from django.contrib import admin
from inventor.core.partners.models import Partner


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('title', 'image')
    search_fields = ('title',)
    readonly_fields = ('created', 'modified')
