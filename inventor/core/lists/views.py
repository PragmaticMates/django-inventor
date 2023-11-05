from bootstrap_modal_forms.generic import BSModalFormView
from bootstrap_modal_forms.utils import is_ajax
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DeleteView
from django.views.generic.detail import SingleObjectMixin, DetailView
from pragmatic.mixins import DeleteObjectMixin

from inventor.core.listings.models.general import Listing
from inventor.core.lists.forms import ListForm
from inventor.core.lists.models import List


class AddToListView(LoginRequiredMixin, SingleObjectMixin, BSModalFormView):
    model = Listing
    form_class = ListForm
    slug_field = 'slug_i18n'
    template_name = 'forms/crispy_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().published().only('id')

    def get_object(self, queryset=None):
        return super().get_object(queryset).get_real_instance()

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs.update({
            'user': self.request.user,
            'listing': self.object
        })
        return form_kwargs

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        if not is_ajax(self.request.META):
            form.save()
        return super().form_valid(form)


class MyListsView(LoginRequiredMixin, ListView):
    model = List

    def get_queryset(self):
        return self.request.user.list_set.all()


# class MyListDeleteView(LoginRequiredMixin, DeleteObjectMixin, DeleteView):
class MyListDeleteView(LoginRequiredMixin, DetailView):
    model = List
    success_url = reverse_lazy('inventor:lists:list_list')
    # template_name = 'confirm_delete.html'

    def get_queryset(self):
        return self.request.user.list_set.all()

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, _('List successfully deleted'))
        return redirect(self.success_url)
