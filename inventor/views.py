from django.contrib.auth import get_user_model
from django.db.models import F
from django.views.generic import TemplateView

from inventor.core.lexicons.models import Locality, Category
from inventor.core.listings.models.general import Listing
from writing.models import Article


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({
            'localities': Locality.objects.all(),
            'categories': Category.objects.without_parent(),
            'articles': Article.objects.published()[:3],
            'users_count': get_user_model().objects.active().count()
        })

        # TODO: refactor to more universal/generic solution
        try:
            from inventor.core.listings.models.listing_types import Accommodation
            context_data.update({
                'top_accommodations': Accommodation.objects
                      # .promoted()
                      .published()
                      .only('id', 'slug', 'title', 'promoted',
                            'locality_id', 'locality__title',
                            'image', 'price', 'price_unit', 'price_starts_at')
                      .annotate(locality_title=F('locality__title'))
                      .order_by('?')[:6],
            })
        except ImportError:
            pass

        return context_data
