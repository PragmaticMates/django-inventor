from django.core.management import BaseCommand
from invoicing.models import Invoice
from openpyxl import Workbook

from tenant.settings.common import project_root


class Command(BaseCommand):
    def handle(self, *args, **options):
        wb = Workbook()

        # grab the active worksheet
        ws = wb.active
        ws.append(['Number', 'Type', 'Status', 'Date issued', 'Date tax point', 'Amount', 'Currency', 'Customer name', 'Customer country'])

        for invoice in Invoice.objects.all():
            ws.append([
                invoice.number,
                invoice.get_type_display(),
                invoice.get_status_display(),
                invoice.date_issue,
                invoice.date_tax_point,
                invoice.total,
                invoice.currency,
                invoice.customer_name,
                invoice.get_customer_country_display()
            ])

        # Save the file
        filepath = project_root('output/invoices.xlsx')
        wb.save(filepath)
