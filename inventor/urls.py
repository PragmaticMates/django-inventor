from inventor.views import HomeView
from django.conf.urls import url

app_name = 'inventor'

urlpatterns = (
    url(r'^$', HomeView.as_view(), name='home'),
)
