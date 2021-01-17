from django.urls import path
from django.utils.translation import pgettext_lazy

from inventor.core.bookings.views import BookingView
from inventor.manager.bookings.views import BookingListView

app_name = 'manager_bookings'

urlpatterns = [
    # path(pgettext_lazy('url', 'book/<str:slug>/'), BookingView.as_view(), name='book_listing')
    path(pgettext_lazy('url', 'bookings/'), BookingListView.as_view(), name='booking_list')
]
