from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import BaseFormView

from inventor.core.newsletters.forms import NewsletterForm
from inventor.core.newsletters.models import Subscriber


class NewsletterView(BaseFormView):
    form_class = NewsletterForm

    def get(self, request, *args, **kwargs):
        return HttpResponseBadRequest()

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['request'] = self.request
        return form_kwargs

    def form_valid(self, form):
        subscription, created = self.save_email(form.cleaned_data['email'])

        if created:
            message = _('New email in newsletter database: %s') % form.cleaned_data['email']

            if not send_mail(
                subject=_('Newsletter form'),
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=not settings.DEBUG
            ):
                messages.error(self.request, _('Failed to sign up. Please try again.'))
                return self.form_invalid(form)

            messages.success(self.request, _("Your e-mail has been successfully saved. Thank you."))
        else:
            messages.info(self.request, _("Thank you! You are already subscribed."))

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _('Failed to send message. Please try again.'))

        for field, errors in form.errors.items():
            if field != '__all__':
                messages.warning(self.request, '{}: {}'.format(field, '. '.join(errors)))
            else:
                messages.warning(self.request, '{}'.format('. '.join(errors)))

        return redirect(self.get_success_url())

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', reverse('inventor:home'))

    def save_email(self, email):
        return Subscriber.objects.get_or_create(email=email)
