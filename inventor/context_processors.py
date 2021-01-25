def cookies_accepted(request):
    cookies_accepted = request.COOKIES.get('isCookieAccepted', 'no') == 'yes'

    return {
        'cookies_accepted': cookies_accepted
    }
