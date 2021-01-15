from django.urls import path
from django.utils.translation import pgettext_lazy

from inventor.core.bookings.views import BookingView

app_name = 'bookings'

urlpatterns = [
    path(pgettext_lazy('url', 'book/<str:slug>/'), BookingView.as_view(), name='book_listing')
]
