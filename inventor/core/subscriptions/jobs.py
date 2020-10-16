from django_rq import job


@job('default')
def send_subscription_reminders(threshold):
    from inventor.core.subscriptions.models import UserPlan

    expiring_plans = UserPlan.objects.expires_in(days=threshold)
    total_plans = expiring_plans.count()
    print(f'Found {total_plans} expiring plans in {threshold} days')

    for user_plan in expiring_plans:
        print(user_plan, user_plan.user, user_plan.plan, user_plan.pricing, user_plan.expiration)
        user_plan.send_reminder()
