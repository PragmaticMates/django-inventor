from collections import OrderedDict
from django.utils.translation import ugettext_lazy as _, ugettext
from outputs.mixins import ExcelExporterMixin
from inventor.core.newsletters.models import Subscriber


class SubscriberXlsxListExporter(ExcelExporterMixin):
    queryset = Subscriber.objects.all()
    filename = _('subscribers.xlsx')

    @staticmethod
    def selectable_fields():
        # attribute, label, width, format (self.FORMATS), value
        return OrderedDict({
            ugettext('Details'): [
                ('email', ugettext('E-mail'), 30),
                # ('subscribed', ugettext('subscribed'), 20, 'datetime'),
            ],
        })

    def __init__(self, **kwargs):
        self.queryset = kwargs.get('queryset')
        super().__init__(**kwargs)

    def get_worksheet_title(self, index=0):
        return ugettext('Subscribers')

    def get_queryset(self):
        return self.queryset

