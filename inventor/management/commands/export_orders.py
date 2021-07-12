from django.core.management import BaseCommand
from openpyxl import Workbook

from commerce.models import Order
from tenant.settings.common import project_root


class Command(BaseCommand):
    def handle(self, *args, **options):
        wb = Workbook()

        # grab the active worksheet
        ws = wb.active
        ws.append(['Number', 'Status', 'User', 'Email', 'Phone', 'Created', 'Modified'])

        for order in Order.objects.select_related('user'):
            ws.append([
                order.number,
                order.get_status_display(),
                str(order.user),
                order.email,
                order.phone,
                order.created,
                order.modified,
            ])

        # Save the file
        filepath = project_root('output/orders.xlsx')
        wb.save(filepath)
