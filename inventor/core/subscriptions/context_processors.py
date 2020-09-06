from django.conf import settings


def user_plan(request):
    plan = None

    if 'inventor.core.subscriptions' in settings.INSTALLED_APPS:
        from inventor.core.subscriptions.models import Plan
        plan = Plan.get_current_plan(request.user)

    return {'user_plan': plan}

