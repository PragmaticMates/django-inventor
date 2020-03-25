import os


def deployment_timestamp(request):
    return {
        'deployment_timestamp': os.environ.get('DEPLOYMENT_TIMESTAMP', None)
    }
