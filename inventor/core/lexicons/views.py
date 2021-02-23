from django.core.validators import EMPTY_VALUES
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse

from inventor.core.lexicons.models import Category
from inventor.core.listings.views import ListingListView


class CategoryDetailView(ListingListView):
    template_name = 'lexicons/category_detail.html'
    lexicon = Category

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(Category, slug_i18n=kwargs.get('slug'))

        # we should redirect from category detail to listing list view if:
        # - filtering by multiple categories
        # - filtering none categories
        # - filtering different category
        # Note: filtering means changing filter. We need to stay on same page if just changing page.

        # redirect to listing list view if needed
        same_referer = request.path in request.META.get('HTTP_REFERER', '')
        requested_categories = request.GET.getlist('categories')
        is_paginating = 'page' in request.GET

        if not is_paginating:
            empty_categories = len(requested_categories) == 0 and same_referer
            multiple_categories = len(requested_categories) > 1
            different_category = len(requested_categories) == 1 and requested_categories[0] != self.category.slug_i18n

            if empty_categories or multiple_categories or different_category:
                params = request.GET.urlencode()
                params = f'?{params}' if params not in EMPTY_VALUES else ''
                url = f"{reverse('listings:listing_list')}{params}"
                return redirect(url)

        self.filter = self.filter_class(**self.get_filter_kwargs())

        # bypass ListingListView.dispatch to prevent redirection loop
        return super(ListingListView, self).dispatch(request, *args, **kwargs)

    def get_filter_kwargs(self):
        filter_kwargs = super().get_filter_kwargs()

        data = filter_kwargs.get('data', {}).copy()

        if self.category.slug_i18n not in data.getlist('categories'):
            data.update({'categories': self.category.slug_i18n})

        filter_kwargs.update({
            'lexicon': self.lexicon,
            'data': data
        })

        return filter_kwargs

    def get_whole_queryset(self):
        return super().get_whole_queryset().of_category(self.category)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data.update({'object': self.category})  # to ensure language switcher functionality
        return context_data
