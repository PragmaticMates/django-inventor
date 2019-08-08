from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from threadedcomments.forms import ThreadedCommentForm


class CommentForm(ThreadedCommentForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'content_type', 'object_pk', 'parent',
            'honeypot', 'timestamp', 'security_hash',
            #'name', 'email', 'url', 'title',
            'comment', 'rating'
        )
        self.fields['comment'].label = ''
        self.fields['comment'].widget.attrs['rows'] = 3
