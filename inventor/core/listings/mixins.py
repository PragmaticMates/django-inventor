from django.utils.text import slugify


class SlugMixin(object):
    MAX_SLUG_LENGTH = 150
    FORCE_SLUG_REGENERATION = True

    def save(self, **kwargs):
        if self.slug != slugify(self.title) or self.FORCE_SLUG_REGENERATION:
            self.slug = slugify(self.title)

        # TODO: Ensure uniqueness

        return super().save(**kwargs)
