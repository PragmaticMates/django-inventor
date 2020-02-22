from django.views.generic import TemplateView

from inventor.core.listings.models.general import Listing


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({'top_listings': Listing.objects.all()})
        return context_data