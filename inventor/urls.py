from django.urls import path

from inventor.core.newsletters.views import NewsletterView
from inventor.views import HomeView

app_name = 'inventor'

urlpatterns = (
    path('', HomeView.as_view(), name='home'),
    path('newsletter/', NewsletterView.as_view(), name='newsletter'),
)
