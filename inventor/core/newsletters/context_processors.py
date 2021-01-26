from inventor.core.newsletters.forms import NewsletterForm


def newsletter_form(request):
    return {
        'newsletter_form': NewsletterForm(request=request, auto_id='newsletter_id_%s')
    }
