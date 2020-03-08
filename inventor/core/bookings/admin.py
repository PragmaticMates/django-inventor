from django.contrib import admin
from inventor.core.bookings.models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('id', 'listing', 'traveler', 'created')
    list_display_links = ('id',)
    autocomplete_fields = ['traveler']
