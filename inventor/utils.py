import hashlib
import random
from datetime import datetime

import django_filters
from crispy_forms.helper import FormHelper


def generate_hash(length=16):
    random_number = str(random.random())
    current_data = str(datetime.now())
    salt = hashlib.sha1(random_number.encode('utf-8')).hexdigest()
    pepper = hashlib.sha1(current_data.encode('utf-8')).hexdigest()
    digest = hashlib.sha1((salt + pepper).encode('utf-8')).hexdigest()
    return digest[:length]


class SingleSubmitFormHelper(FormHelper):  # TODO: move to django-pragmatic
    def __init__(self, form=None):
        super().__init__(form)
        self.attrs['onsubmit'] = "submit.disabled=true; return true;"


class PositiveBooleanFilter(django_filters.BooleanFilter):   # TODO: move to django-pragmatic
    def filter(self, qs, value):
        if not value:
            return qs
        return super().filter(qs, value)
