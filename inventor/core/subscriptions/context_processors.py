from django.conf import settings
from inventor.core.subscriptions.models import Plan


def user_plan(request):
    plan = Plan.get_current_plan(request.user) if 'inventor.core.subscriptions' in settings.INSTALLED_APPS else None
    return {'user_plan': plan}

