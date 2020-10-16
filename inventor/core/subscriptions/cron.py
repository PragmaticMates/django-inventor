def send_subscription_reminders():
    from inventor.core.subscriptions import jobs
    jobs.send_subscription_reminders.delay(7)
    jobs.send_subscription_reminders.delay(1)
