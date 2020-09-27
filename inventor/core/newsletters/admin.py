from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

from inventor.core.newsletters.exporters import SubscriberXlsxListExporter
from inventor.core.newsletters.models import Subscriber


@admin.register(Subscriber)
class SubscriptionModel(admin.ModelAdmin):
    date_hierarchy = 'subscribed'
    list_display = ['email', 'subscribed']
    actions = ['sync_with_accounts', 'export_to_xls', 'export_to_list']

    def sync_with_accounts(self, request, queryset):
        unsubscribed_emails = get_user_model().objects.filter(agree_marketing_purposes=False).values_list('email', flat=True)
        unsubscribed_subscribers = Subscriber.objects.filter(email__in=list(unsubscribed_emails))
        unsubscribed_subscribers_count = unsubscribed_subscribers.count()
        unsubscribed_subscribers.delete()

        already_subscribed_subscribers = Subscriber.objects.all()
        already_subscribed_subscribers_count_before = already_subscribed_subscribers.count()

        for user in get_user_model().objects\
                .active()\
                .filter(agree_marketing_purposes=True)\
                .exclude(email__in=already_subscribed_subscribers.values_list('email', flat=True)):

            Subscriber.objects.get_or_create(email=user.email)

        already_subscribed_subscribers_count_after = Subscriber.objects.all().count()
        new_subscribers = already_subscribed_subscribers_count_after - already_subscribed_subscribers_count_before
        
        messages.info(request, _('Deleted subscribers: %d. New subscribers: %s') % (unsubscribed_subscribers_count, new_subscribers))

    def export_to_xls(self, request, queryset):
        # emails = list(queryset.values('email'))
        # from pprint import pprint
        # pprint(emails)
        # from django.core.mail import send_mail
        # send_mail(subject='subscribers', message=str(emails), recipient_list=[request.user.email], from_email=None)
        # messages.info(request, _('Export has been sent to your e-mail address'))
        exporter = SubscriberXlsxListExporter(queryset=queryset, user=request.user, recipients=[request.user], selected_fields=['email'])
        return exporter.export_to_response()

    def export_to_list(self, request, queryset):
        return HttpResponse('<br>'.join(queryset.values_list('email', flat=True)))
