from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from inventor.core.bookings.models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('id', 'listing', 'get_book_from_display', 'get_book_to_display', 'number_of_persons',
                    'person', 'phone', 'email', 'created')
    list_display_links = ('id',)
    autocomplete_fields = ['traveler']
    actions = ['send_request']

    def send_request(self, request, queryset):
        for booking in queryset:
            booking.send_request()


class BookingMixinAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Booking'), {'fields': ('booking_enabled', ('booking_period', 'booking_min_period', 'booking_max_period'), ('booking_min_persons', 'capacity'))}),
    )
