import django_rq
from django.apps import AppConfig
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from inventor.core.subscriptions.cron import send_subscription_reminders


class Config(AppConfig):
    name = 'inventor.core.subscriptions'
    verbose_name = _('Subscriptions')

    def schedule_jobs(self):
        scheduler = django_rq.get_scheduler('cron')

        # Cron task to send subscription reminders
        scheduler.cron(
            "0 9 * * *",  # Run every day at 9:00 [UTC]
            # "* * * * *",  # Run every minute
            func=send_subscription_reminders,
            timeout=settings.RQ_QUEUES['cron']['DEFAULT_TIMEOUT']
        )
