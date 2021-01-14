from django.db.models import F
from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView
from inventor.core.lexicons.models import Locality, Category
from inventor.core.listings.models.general import Listing
from inventor.templatetags.inventor import uri
from writing.models import Article


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({
            'localities': Locality.objects.all(),
            'categories': Category.objects.without_parent(),
            'articles': Article.objects.highlighted().order_by('-created')[:3],
        })

        # TODO: refactor to more universal/generic solution: move to template tag?
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


@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: *",
        # "Disallow: /private/",
        f"Sitemap: {uri({'request': request}, reverse('sitemap'))}",
    ]

    # for hidden_listing in Listing.objects.hidden():
    #     lines.append(f"Disallow: {hidden_listing.get_absolute_url()}")

    return HttpResponse("\n".join(lines), content_type="text/plain")
