from django.views.generic import ListView, DetailView

from inventor.core.subscriptions.models import Plan, UserPlan


class PlanListView(ListView):
    model = Plan


class UserPlanDetailView(DetailView):
    model = UserPlan

    def get_object(self, queryset=None):
        try:
            return self.request.user.subscription
        except AttributeError:
            return None
