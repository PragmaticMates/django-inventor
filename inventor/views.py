from django.db.models import F
from django.views.generic import TemplateView

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
                      'location_id', 'location__title',
                      'image', 'price', 'price_unit', 'price_starts_at')
                .annotate(location_title=F('location__title'))
                .order_by('?')[:6]
        })
        return context_data
