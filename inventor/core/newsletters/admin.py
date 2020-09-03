from django.contrib import admin

from inventor.core.newsletters.models import Subscriber


@admin.register(Subscriber)
class SubscriptionModel(admin.ModelAdmin):
    date_hierarchy = 'subscribed'
    list_display = ['email', 'subscribed']
