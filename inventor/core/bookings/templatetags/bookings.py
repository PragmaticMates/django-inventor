from django import template

from inventor.core.bookings.forms import BookingForm

register = template.Library()


@register.simple_tag(takes_context=True)
def booking_form(context, listing):
    request = context['request']
    form = BookingForm(listing, data=request.POST if request.method == 'POST' else None)
    return form
