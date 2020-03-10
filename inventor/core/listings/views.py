from django.db.models import F
from django.views.generic import ListView, DetailView
from inventor.core.listings.filters import ListingFilter
from inventor.core.listings.models.general import Listing


class ListingListView(ListView):
    model = Listing
    filter_class = ListingFilter
    paginate_by = 12

    def dispatch(self, request, *args, **kwargs):
        self.filter = self.filter_class(data=request.GET, queryset=self.get_whole_queryset(), listing_type=None if self.model == Listing else self.model)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.filter.qs.only('id', 'slug', 'title', 'location_id', 'location__title', 'image', 'price', 'price_unit', 'price_starts_at', 'promoted').annotate(location_title=F('location__title'))
        return queryset
        # return self.sort_queryset(queryset)

    def get_whole_queryset(self):
        return super().get_queryset().select_subclasses().order_by('-promoted', 'modified')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({
            'title': self.model._meta.verbose_name_plural,
            'filter': self.filter
        })
        return context_data


class ListingDetailView(DetailView):
    model = Listing
    template_name = 'listings/listing_detail.html'

    # def get_queryset(self):
    #     return super().get_queryset().select_subclasses()

    def get_queryset(self):
        return super().get_queryset().only('id')

    def get_object(self, queryset=None):
        return super().get_object(queryset).get_real_instance()
