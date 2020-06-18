from django.urls import path
from django.utils.translation import pgettext_lazy
from inventor.core.accounts.views import UserDashboardView, UpdateProfileView

app_name = 'accounts'

urlpatterns = [
    path(pgettext_lazy("url", 'dashboard/'), UserDashboardView.as_view(), name='user_dashboard'),
    path(pgettext_lazy("url", 'profile/'), UpdateProfileView.as_view(), name='user_update_profile'),
]
