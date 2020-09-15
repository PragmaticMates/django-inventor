from django.conf import settings
from django.urls import path, include

from inventor.core.newsletters.views import NewsletterView
from inventor.views import HomeView
from django.utils.translation import pgettext_lazy

app_name = 'inventor'

urlpatterns = (
    path('', HomeView.as_view(), name='home'),
    path('newsletter/', NewsletterView.as_view(), name='newsletter'),
    path(pgettext_lazy('url', 'accounts/'), include('inventor.core.accounts.urls', namespace='accounts')),
)

if 'inventor.core.subscriptions' in settings.INSTALLED_APPS:
    urlpatterns += (
        path('subscriptions/', include('inventor.core.subscriptions.urls', namespace='subscriptions')),
    )
