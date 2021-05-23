from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django_comments.signals import comment_was_posted


def thank_user(sender, comment=None, request=None, **kwargs):
    messages.add_message(request, messages.SUCCESS, _('You comment has been posted!'))
comment_was_posted.connect(thank_user)
