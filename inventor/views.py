from django.views.generic import TemplateView

from inventor.core.listings.models.listing_types import Accommodation


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({'top_accommodations': Accommodation.objects.promoted().select_subclasses().select_related('location')})
        return context_data
