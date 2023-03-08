from bootstrap_modal_forms.forms import BSModalForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Div
from django import forms

from inventor.forms import ModalContentLayout


class ListForm(BSModalForm):
    # TODO translate
    modal_title = 'Title'
    modal_submit = 'Submit'
    modal_message = 'Ola ?'

    title = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.helper = SingleSubmitFormHelper()
        self.helper = FormHelper()
        self.helper.layout = self.get_layout()

    def get_layout(self):
        return Layout(
            ModalContentLayout(
                Row(
                    Div('title', css_class='col-md-6'),
                ),
                modal_title=self.modal_title,
                modal_submit=self.modal_submit,
                modal_message=self.modal_message,
                modal_close=True,
            )
        )
