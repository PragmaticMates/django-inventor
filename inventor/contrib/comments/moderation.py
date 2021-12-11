from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader
from django.utils.translation import ugettext_lazy as _
from django_comments.moderation import CommentModerator

from icecream import ic


class ListingCommentModerator(CommentModerator):
    email_notification = True

    def email(self, comment, content_object, request):
        """
        Send email notification of a new comment to site staff when email
        notifications have been requested.

        """
        if not self.email_notification:
            return

        # TODO: refactor to notifications
        recipient_list = [user.email for user in get_user_model().objects.active().staff()]
        ic(f'Sending comment for {content_object} to {recipient_list}')

        t = loader.get_template('comments/comment_notification_email.txt')
        c = {
            'comment': comment,
            'content_object': content_object,
        }
        subject = _('[%(site)s] New comment posted on "%(object)s"') % {
            'site': get_current_site(request).name,
            'object': content_object,
        }
        message = t.render(c)

        # TODO: use MailManager
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=True)
