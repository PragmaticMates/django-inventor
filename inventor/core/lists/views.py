from bootstrap_modal_forms.generic import BSModalUpdateView, BSModalFormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from inventor.core.listings.models.general import Listing

from inventor.core.lists.forms import ListForm


class ListFormView(LoginRequiredMixin, SingleObjectMixin, BSModalFormView):
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

    # def get_form_kwargs(self):
    #     form_kwargs = super().get_form_kwargs()
    #     form_kwargs.update({'listing': self.object})
    #     return form_kwargs

