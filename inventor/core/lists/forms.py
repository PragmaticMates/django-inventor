from bootstrap_modal_forms.forms import BSModalForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Div
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EMPTY_VALUES
from django.forms import HiddenInput
from django.utils.translation import ugettext_lazy as _

from inventor.core.lists.models import List
from inventor.forms import ModalContentLayout


class ListForm(BSModalForm):
    modal_title = _('Add to list')
    modal_submit = _('Submit')
    modal_message = _('Choose from existing lists or create a new one:')
    lists = forms.ModelMultipleChoiceField(queryset=List.objects.all(), widget=forms.CheckboxSelectMultiple)
    new_list_title = forms.CharField(label=_('New list'), required=False)

    def __init__(self, user, listing, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.listing = listing

        # self.helper = SingleSubmitFormHelper()
        self.helper = FormHelper()
        self.helper.layout = self.get_layout()
        user_lists = user.list_set.all()

        if user_lists.exists():
            self.fields['lists'].queryset = user.list_set.all()
            self.fields['lists'].initial = listing.list_set.all()
        else:
            self.modal_message = _("You don't have any list yet. Create a new one.'")
            self.fields['lists'].widget = HiddenInput()
            self.fields['new_list_title'].required = True

    def get_layout(self):
        return Layout(
            ModalContentLayout(
                Row(
                    Div('lists', css_class='col-12'),
                    Div('new_list_title', css_class='col-12'),
                ),
                modal_title=self.modal_title,
                modal_submit=self.modal_submit,
                modal_message=self.modal_message,
                modal_close=True,
            )
        )

    def clean_new_list_title(self):
        new_list_title = self.cleaned_data.get('new_list_title')
        if self.user.list_set.filter(title=new_list_title).exists():
            raise ValidationError(_('List with such title already exists'))
        return new_list_title

    def save(self, *args, **kwargs):
        print('Save')
        # user_lists = self.user.list_set.all()
        lists = self.cleaned_data['lists']

        self.listing.lists.remove()
        self.listing.lists.add(lists)

        new_list_title = self.cleaned_data.get('new_list_title')

        if new_list_title not in EMPTY_VALUES:
            new_list = List.objects.get_or_create(user=self.user, title=new_list_title)
            self.listing.lists.add(new_list)
