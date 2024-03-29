from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from threadedcomments.models import ThreadedComment


class ReviewComment(ThreadedComment):
    RATING_MIN = 1
    RATING_MAX = 5
    rating = models.PositiveSmallIntegerField(_('rating'),
        validators=[MinValueValidator(RATING_MIN), MaxValueValidator(RATING_MAX)],
        blank=True, null=True, default=None)


from .signals import *  # TODO: move to apps.py
