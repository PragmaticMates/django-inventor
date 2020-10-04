from django.views.generic import ListView

from inventor.core.partners.models import Partner


class PartnerListView(ListView):
    model = Partner
