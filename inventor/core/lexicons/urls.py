from django.urls import path
from django.utils.translation import pgettext_lazy

from inventor.core.lexicons.views import CategoryDetailView

app_name = 'lexicons'

urlpatterns = []

# listing detail
urlpatterns.append(path(pgettext_lazy('url', 'category/<str:slug>/'), CategoryDetailView.as_view(), name='category_detail'))
