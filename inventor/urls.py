from django.urls import path, include

from inventor.core.newsletters.views import NewsletterView
from inventor.views import HomeView

app_name = 'inventor'

urlpatterns = (
    path('', HomeView.as_view(), name='home'),
    path('newsletter/', NewsletterView.as_view(), name='newsletter'),
    path('accounts/', include('inventor.core.accounts.urls', namespace='accounts')),
)
