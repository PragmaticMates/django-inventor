import os


def deployment_timestamp(request):  # TODO: move to django-pragmatic
    return {
        'deployment_timestamp': os.environ.get('DEPLOYMENT_TIMESTAMP', None)
    }


def settings(request):  # TODO: move to django-pragmatic
    import django

    return {
        'settings': django.conf.settings
    }
