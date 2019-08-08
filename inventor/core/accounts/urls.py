from django.conf.urls import url
from django.utils.translation import pgettext_lazy
from inventor.core.accounts.views import UserDetailView, UpdateProfileView, UserUpdateView, \
    UserCreateView, UserDeleteView  # UserListView

app_name = 'accounts'

urlpatterns = [
    url(pgettext_lazy("url", r'^users/(?P<pk>[-\d]+)/$'), UserDetailView.as_view(), name='user_detail'),
    url(pgettext_lazy("url", r'^users/(?P<pk>[-\d]+)/update/$'), UserUpdateView.as_view(), name='user_update'),
    url(pgettext_lazy("url", r'^users/(?P<pk>[-\d]+)/delete/$'), UserDeleteView.as_view(), name='user_delete'),
    url(pgettext_lazy("url", r'^users/(?P<pk>[-\d]+)/changelog/$'), UserDetailView.as_view(template_name_suffix='_changelog'), name='user_changelog'),
    url(pgettext_lazy("url", r'^users/update/profile/$'), UpdateProfileView.as_view(), name='user_update_profile'),
    url(pgettext_lazy("url", r'^users/create/$'), UserCreateView.as_view(), name='user_create'),
    # url(pgettext_lazy("url", r'^users/$'), UserListView.as_view(), name='user_list'),
]
