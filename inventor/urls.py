from django.conf import settings
from django.urls import path, include

from inventor.core.newsletters.views import NewsletterView
from inventor.core.partners.views import PartnerListView
from inventor.views import HomeView
from django.utils.translation import pgettext_lazy

app_name = 'inventor'

urlpatterns = (
    path('', HomeView.as_view(), name='home'),
    path('', include('inventor.core.lexicons.urls', namespace='lexicons')),
    path('newsletter/', NewsletterView.as_view(), name='newsletter'),
    path(pgettext_lazy('url', 'partners/'), PartnerListView.as_view(), name='partners'),
    path(pgettext_lazy('url', 'accounts/'), include('inventor.core.accounts.urls', namespace='accounts')),
    path(pgettext_lazy('url', 'bookings/'), include('inventor.core.bookings.urls', namespace='bookings')),
    path(pgettext_lazy('url', 'manager/'), include('inventor.manager.urls', namespace='manager')),
)

if 'inventor.core.subscriptions' in settings.INSTALLED_APPS:
    urlpatterns += (
        path(pgettext_lazy('url', 'subscriptions/'), include('inventor.core.subscriptions.urls', namespace='subscriptions')),
    )
