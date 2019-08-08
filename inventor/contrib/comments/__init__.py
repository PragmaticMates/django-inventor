def get_model():
    from inventor.contrib.comments.models import ReviewComment
    return ReviewComment


def get_form():
    from inventor.contrib.comments.forms import CommentForm
    return CommentForm
