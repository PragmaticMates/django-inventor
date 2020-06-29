from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from commerce import settings as commerce_settings
from commerce.managers import PaymentManager as CommercePaymentManager
from commerce.models import Payment


class PaymentManager(CommercePaymentManager):
    def render_payment_button(self):
        if self.order.payment_method.method == Payment.METHOD_WIRE_TRANSFER:
            template = get_template('commerce/payment_button_wire_transfer.html')
            return template.render({'order': self.order, 'iban': commerce_settings.IBAN })

        label = _('Pay')
        return mark_safe(f'<a href="{self.order.get_payment_url()}">{label}</a>')
