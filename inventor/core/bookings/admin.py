from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from inventor.core.bookings.models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('id', 'listing', 'traveler', 'created')
    list_display_links = ('id',)
    autocomplete_fields = ['traveler']


class BookingMixinAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Booking'), {'fields': ('bookings_enabled', ('booking_period', 'bookings_min_period', 'bookings_max_period'), ('bookings_min_persons', 'capacity'))}),
    )
