from django.urls import path
from django.utils.translation import pgettext_lazy
from inventor.core.subscriptions.views import PlanListView

app_name = 'subscriptions'

urlpatterns = [
    path(pgettext_lazy("url", 'plans/'), PlanListView.as_view(), name='plans'),
]
