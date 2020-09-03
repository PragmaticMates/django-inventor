from django.views.generic import ListView

from inventor.core.subscriptions.models import Plan


class PlanListView(ListView):
    model = Plan
