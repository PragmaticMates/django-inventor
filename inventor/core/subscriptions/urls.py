from django.urls import path
from django.utils.translation import pgettext_lazy
from inventor.core.subscriptions.views import PlanListView, UserPlanDetailView

app_name = 'subscriptions'

urlpatterns = [
    path(pgettext_lazy("url", 'plans/'), PlanListView.as_view(), name='plans'),
    path(pgettext_lazy("url", 'my-plan/'), UserPlanDetailView.as_view(), name='user_plan'),
]
