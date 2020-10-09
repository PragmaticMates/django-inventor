from allauth.account.adapter import DefaultAccountAdapter
from django.core.cache import cache
from django.core.validators import EMPTY_VALUES


class RedirectionAccountAdapter(DefaultAccountAdapter):
    def get_cache_key(self, user):
        return f'signup-next-url-{user.pk}'

    def save_next_url(self, request, user):
        next = request.POST.get('next', None)  # TODO: parameter
        if next not in EMPTY_VALUES:
            # save redirection URL into cache
            cache_key = self.get_cache_key(user)
            timeout = 60 * 60 * 24 * 3  # 3 days  # TODO: activation link expiration
            cache.set(cache_key, next, timeout=timeout)

    def get_next_url(self, user):
        cache_key = self.get_cache_key(user)
        return cache.get(cache_key) if cache.has_key(cache_key) else None

    # def get_login_redirect_url(self, request):
    #     return super().get_login_redirect_url(request)

    def get_email_confirmation_redirect_url(self, request):
        """
        The URL to return to after successful e-mail confirmation.
        """
        if request.user.is_authenticated:
            next_url = self.get_next_url(request.user)

            if next_url:
                cache.delete(self.get_cache_key(request.user))
                return next_url

        return super().get_email_confirmation_redirect_url(request)

    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        user = super().save_user(request, user, form, commit)
        self.save_next_url(request, user)
        return user
