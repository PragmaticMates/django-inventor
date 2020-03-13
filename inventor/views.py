from django.db.models import F
from django.views.generic import TemplateView

from inventor.core.lexicons.models import Locality
from inventor.core.listings.models.listing_types import Accommodation


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({
            'top_accommodations': Accommodation.objects
                # .promoted()
                .select_subclasses()
                .only('id', 'slug', 'title', 'promoted',
                      'locality_id', 'locality__title',
                      'image', 'price', 'price_unit', 'price_starts_at')
                .annotate(locality_title=F('locality__title'))
                .order_by('?')[:6],
            'localities': Locality.objects.all()
        })
        return context_data
