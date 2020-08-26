from django.template.loader import get_template
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from inventor.templatetags.inventor import uri

from commerce import settings as commerce_settings
from commerce.managers import PaymentManager as CommercePaymentManager
from commerce.models import Payment


class PaymentManager(CommercePaymentManager):
    def render_payment_button(self):
        if self.order.payment_method.method == Payment.METHOD_WIRE_TRANSFER:
            template = get_template('commerce/payment_button_wire_transfer.html')
            return template.render({'order': self.order})

        if self.order.payment_method.method == Payment.METHOD_ONLINE_PAYMENT:
            label = _('Pay')
            return mark_safe(f'<a href="{self.order.get_payment_url()}" class="btn btn-primary">{label}</a>')

        raise NotImplementedError()

    def render_payment_information(self):
        if self.order.payment_method.method == Payment.METHOD_WIRE_TRANSFER:
            template = get_template('commerce/payment_information_wire_transfer.html')
            return template.render({'order': self.order, 'commerce_settings': commerce_settings})

        return ''

    def get_online_payment_url(self, order):
        from commerce.gateways.globalpayments.models import Order as GPOrder
        GPOrder.objects.create(order=order)

        payment_data = {
            'order': order,
            'MERCHANTNUMBER': commerce_settings.GATEWAY_GP_MERCHANT_NUMBER,
            'OPERATION': 'CREATE_ORDER',
            'ORDERNUMBER': order.order_set.latest().id,
            'AMOUNT': order.total_in_cents,
            'CURRENCY': '',  # empty value is default value of payment gateway merchant eshop
            'DEPOSITFLAG': 1,
            'MERORDERNUM': order.number,
            'URL': uri({}, order.get_payment_return_url()),  # absolute URL
            'REFERENCENUMBER': order.id
        }

        digest = self.get_digest(payment_data)
        payment_data.update({'DIGEST': digest})

        params = urlencode(payment_data)
        url = commerce_settings.GATEWAY_GP_URL_TEST
        payment_url = f'{url}?{params}'
        return payment_url

    def get_digest(self, payment_data):
        from OpenSSL import crypto
        import base64

        d = payment_data

        # MERCHANTNUMBER + | + OPERATION + | + ORDERNUMBER + | + AMOUNT + | + CURRENCY + | + DEPOSITFLAG + | + MERORDERNUM + | + URL + | + REFERENCENUMBER
        digest_input = f'{d["MERCHANTNUMBER"]}|{d["OPERATION"]}|{d["ORDERNUMBER"]}|{d["AMOUNT"]}|{d["CURRENCY"]}|{d["DEPOSITFLAG"]}|{d["MERORDERNUM"]}|{d["URL"]}|{d["REFERENCENUMBER"]}'

        private_key = {
            'path': commerce_settings.GATEWAY_GP_PRIVATE_KEY_PATH,
            'password': commerce_settings.GATEWAY_GP_PRIVATE_KEY_PASSWORD
        }

        with open(private_key['path'], "r") as key_file:
            key = key_file.read()

        password = private_key['password'].encode('ascii')

        pkey = crypto.load_privatekey(crypto.FILETYPE_PEM, key, password)
        sign = crypto.sign(pkey, digest_input, "sha1")
        data_base64 = base64.b64encode(sign)
        digest = data_base64.decode("utf-8")
        return digest
