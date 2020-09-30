from rest_framework import serializers, viewsets

from invoicing.models import Invoice, Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['title', 'quantity', 'unit', 'unit_price', 'discount', 'tax_rate', 'tag', 'weight']


class InvoiceSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, source='item_set')

    class Meta:
        model = Invoice
        extra_kwargs = {
            'url': {'view_name': 'api:invoice-detail'},
        }
        fields = (
            'type', 'status',
            'sequence', 'number',
            'subtitle', 'related_document',
            'language', 'note',
            'currency',
            'reference',
            'attachments',
            'items'
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        ret['amounts'] = {
            'credit': instance.credit,
            'total': instance.total,
            'vat': instance.vat,
        }

        ret['methods'] = {
            'payment': instance.payment_method,
            'delivery': instance.delivery_method,
        }

        ret['dates'] = {
            'issue': instance.date_issue,
            'tax_point': instance.date_tax_point,
            'due': instance.date_due,
            'sent': instance.date_sent,
            'paid': instance.date_paid,
            'reminder_sent': instance.date_reminder_sent,
        }

        ret['symbols'] = {
            'constant': instance.constant_symbol,
            'variable': instance.variable_symbol,
            'specific': instance.specific_symbol,
        }

        ret['bank'] = {
            'name': instance.bank_name,
            'street': instance.bank_street,
            'zip': instance.bank_zip,
            'city': instance.bank_city,
            'country': instance.bank_country.code,
            'iban': instance.bank_iban,
            'swift_bic': instance.bank_swift_bic,
        }

        ret['supplier'] = {
            'name': instance.supplier_name,
            'street': instance.supplier_street,
            'zip': instance.supplier_zip,
            'city': instance.supplier_city,
            'country': instance.supplier_country.code,
            'registration_id': instance.supplier_registration_id,
            'tax_id': instance.supplier_tax_id,
            'vat_id': instance.supplier_vat_id,
            'additional_info': instance.supplier_additional_info,
        }

        ret['issuer'] = {
            'name': instance.issuer_name,
            'email': instance.issuer_email,
            'phone': instance.issuer_phone,
        }

        ret['customer'] = {
            'name': instance.customer_name,
            'street': instance.customer_street,
            'zip': instance.customer_zip,
            'city': instance.customer_city,
            'country': instance.customer_country.code,
            'registration_id': instance.customer_registration_id,
            'tax_id': instance.customer_tax_id,
            'vat_id': instance.customer_vat_id,
            'additional_info': instance.customer_additional_info,
            'email': instance.customer_email,
            'phone': instance.customer_phone,
        }

        ret['shipping'] = {
            'name': instance.shipping_name,
            'street': instance.shipping_street,
            'zip': instance.shipping_zip,
            'city': instance.shipping_city,
            'country': instance.shipping_country.code,
        }

        return ret


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all() \
        .prefetch_related('item_set')
    serializer_class = InvoiceSerializer

