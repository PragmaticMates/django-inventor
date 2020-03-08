from django.utils.text import slugify


class SlugMixin(object):
    MAX_SLUG_LENGTH = 150
    FORCE_SLUG_REGENERATION = True

    def save(self, **kwargs):
        if self.slug != slugify(self.title) or self.FORCE_SLUG_REGENERATION:
            slug = slugify(self.title)
            self.slug = slug
            index = 1

            # Ensure uniqueness
            while self.__class__.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f'{slug}-{index}'
                index += 1

        return super().save(**kwargs)
