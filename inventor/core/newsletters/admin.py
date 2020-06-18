from django.contrib import admin

from inventor.core.newsletters.models import Subscription


@admin.register(Subscription)
class SubscriptionModel(admin.ModelAdmin):
    date_hierarchy = 'subscribed'
    list_display = ['email', 'subscribed']
