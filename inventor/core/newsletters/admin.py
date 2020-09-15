from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from inventor.core.newsletters.exporters import SubscriberXlsxListExporter
from inventor.core.newsletters.models import Subscriber


@admin.register(Subscriber)
class SubscriptionModel(admin.ModelAdmin):
    date_hierarchy = 'subscribed'
    list_display = ['email', 'subscribed']
    actions = ['sync_with_accounts', 'export']

    def sync_with_accounts(self, request, queryset):
        for user in get_user_model().objects.active():
            Subscriber.objects.get_or_create(email=user.email)

    def export(self, request, queryset):
        # emails = list(queryset.values('email'))
        # from pprint import pprint
        # pprint(emails)
        # from django.core.mail import send_mail
        # send_mail(subject='subscribers', message=str(emails), recipient_list=[request.user.email], from_email=None)
        # messages.info(request, _('Export has been sent to your e-mail address'))
        exporter = SubscriberXlsxListExporter(queryset=queryset, user=request.user, recipients=[request.user], selected_fields=['email'])
        return exporter.export_to_response()
