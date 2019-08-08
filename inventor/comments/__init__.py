def get_model():
    from inventor.comments.models import ReviewComment
    return ReviewComment


def get_form():
    from inventor.comments.forms import CommentForm
    return CommentForm
