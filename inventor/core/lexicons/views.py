from inventor.core.lexicons.models import Category
from inventor.core.listings.views import ListingListView


class CategoryDetailView(ListingListView):
    template_name = 'lexicons/category_detail.html'
    lexicon = Category

    def dispatch(self, request, *args, **kwargs):
        self.category = Category.objects.get(slug_i18n=kwargs.get('slug'))
        return super().dispatch(request, *args, **kwargs)

    def get_filter_kwargs(self):
        filter_kwargs = super().get_filter_kwargs()
        filter_kwargs.update({
            'lexicon': self.lexicon
        })
        return filter_kwargs

    def get_whole_queryset(self):
        return super().get_whole_queryset().of_category(self.category)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({'object': self.category})  # to ensure language switcher functionality
        return context_data
