from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin

from inventor.core.bookings.forms import BookingForm
from inventor.core.listings.models.general import Listing


class BookingView(SingleObjectMixin, FormView):
    model = Listing
    form_class = BookingForm
    slug_field = 'slug_i18n'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().published().only('id')

    def get_object(self, queryset=None):
        return super().get_object(queryset).get_real_instance()

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs.update({'listing': self.object})
        return form_kwargs

    def form_valid(self, form):
        # TODO: save to DB
        # TODO: send message
        messages.success(self.request, 'Your request has been successfully sent to listing owner.')
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        messages.error(self.request, 'An error occurred while processing your request. Please try again.')
        return redirect(self.get_success_url())

    def get_success_url(self):
        return self.object.get_absolute_url()

