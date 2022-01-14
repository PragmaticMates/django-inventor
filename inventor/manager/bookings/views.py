from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView
from pragmatic.mixins import DisplayListViewMixin, SortingListViewMixin

from inventor.core.bookings.models import Booking


class BookingListView(DisplayListViewMixin, SortingListViewMixin, ListView):
    model = Booking
    template_name = 'manager/bookings/booking_list.html'
    # filter_class = ListingFilter
    paginate_by = 12
    displays = ['rows']
    paginate_by_display = {'rows': [12, 24, 48]}
    sorting_options = {
        '-created': _('Newest'),
        'created': _('Oldest'),
    }

    # def get_sorting_options(self):
    #     return {**{'-promoted': (_('Promoted'), ['-promoted', 'created'])}, **self.sorting_options}

    def dispatch(self, request, *args, **kwargs):

        # self.filter = self.filter_class(**self.get_filter_kwargs())
        return super().dispatch(request, *args, **kwargs)

    # def get_filter_kwargs(self):
    #     return {
    #         'data': self.request.GET,
    #         'queryset': self.get_whole_queryset(),
    #         'listing_type': None if self.model == Listing else self.model,
    #     }

    def get_template_names(self):
        names = super().get_template_names()
        names.insert(1, f"manager/bookings/booking{self.template_name_suffix}.html")
        return names

    # def get_queryset(self):
    #     queryset = self.filter.qs\
    #         .annotate(locality_title=F('locality__title'))\
    #         .prefetch_related('categories')
    #     return self.sort_queryset(queryset)

    # def get_whole_queryset(self):
    #     qs = super().get_queryset()\
    #         .published()\
    #         .not_hidden()\
    #         .order_by('-promoted', 'modified')
    #
    #     if self.model == Listing:
    #         qs = qs.select_subclasses()
    #
    #     return qs

    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #     context_data.update({
    #         'title': self.model._meta.verbose_name_plural,
    #         'filter': self.filter
    #     })
    #     return context_data


# class BookingView(SingleObjectMixin, FormView):
#     model = Listing
#     form_class = BookingForm
#     slug_field = 'slug_i18n'
#
#     def dispatch(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         return super().dispatch(request, *args, **kwargs)
#
#     def get_queryset(self):
#         return super().get_queryset().published().only('id')
#
#     def get_object(self, queryset=None):
#         return super().get_object(queryset).get_real_instance()
#
#     def get_form_kwargs(self):
#         form_kwargs = super().get_form_kwargs()
#         form_kwargs.update({'listing': self.object})
#         return form_kwargs
#
#     def form_valid(self, form):
#         # TODO: save to DB
#         # TODO: send message
#         messages.success(self.request, 'Your request has been successfully sent to listing owner.')
#         return super().form_valid(form)
#
#     def form_invalid(self, form):
#         print(form.errors)
#         messages.error(self.request, 'An error occurred while processing your request. Please try again.')
#         return redirect(self.get_success_url())
#
#     def get_success_url(self):
#         return self.object.get_absolute_url()
#
