from datetime import timedelta

from django.db import models
from django.utils.timezone import now


class PlanQuerySet(models.QuerySet):
    def visible(self):
        return self.filter(is_visible=True)


class UserPlanQuerySet(models.QuerySet):
    def expires_in(self, days=7):
        threshold = now() - timedelta(days=days)
        return self.filter(expiration=threshold.date())
