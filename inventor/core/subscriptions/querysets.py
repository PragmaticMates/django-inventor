from django.db import models


class PlanQuerySet(models.QuerySet):
    def visible(self):
        return self.filter(is_visible=True)
