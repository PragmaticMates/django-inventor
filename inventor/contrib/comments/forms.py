from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div

from inventor.contrib.comments import get_model
from threadedcomments.forms import ThreadedCommentForm


class ReviewCommentForm(ThreadedCommentForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'content_type', 'object_pk', 'parent',
            Div('honeypot', css_class='d-none'), 'timestamp', 'security_hash',
            #'name', 'email', 'url', 'title',
            'comment', 'rating'
        )
        self.fields['comment'].label = ''
        self.fields['comment'].widget.attrs['rows'] = 3

    def get_comment_model(self):
        return get_model()

    def get_comment_create_data(self, **kwargs):
        data = super().get_comment_create_data(**kwargs)
        data['rating'] = self.cleaned_data.get('rating', None)
        return data
