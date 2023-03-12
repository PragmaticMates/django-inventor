from django.urls import path
from django.utils.translation import pgettext_lazy

from inventor.core.lists.views import AddToListView, MyListsView

app_name = 'lists'

urlpatterns = [
    path(pgettext_lazy('url', 'add-to-list/<str:slug>/'), AddToListView.as_view(), name='list_listing'),
    path('', MyListsView.as_view(), name='list_list')
]
