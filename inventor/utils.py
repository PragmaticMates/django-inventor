def get_comment_model():
    from django.conf import settings
    comments_app = getattr(settings, 'COMMENTS_APP', 'django_comments')