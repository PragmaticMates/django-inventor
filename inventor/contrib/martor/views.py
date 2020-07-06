import json
import os
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Q
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from martor.utils import LazyEncoder

from inventor.contrib.martor.utils import scale_down_image, rotate_jpeg_by_exif


@login_required
def markdown_search_user(request):
    """
    Json usernames of the users registered & actived.
    url(method=get):
        /martor/search-user/?username={username}
    Response:
        error:
            - `status` is status code (204)
            - `error` is error message.
        success:
            - `status` is status code (204)
            - `data` is list dict of usernames.
                { 'status': 200,
                  'data': [
                    {'usernane': 'john'},
                    {'usernane': 'albert'}]
                }
    """
    data = {}
    username = request.GET.get('username')
    if username is not None \
            and username != '' \
            and ' ' not in username:

        user_model = get_user_model()
        username_field = user_model.USERNAME_FIELD

        users = user_model.objects.filter(
            Q(**{'{}__icontains'.format(username_field): username})
        ).filter(is_active=True)
        if users.exists():
            data.update({
                'status': 200,
                'data': [{'username': getattr(u, username_field)} for u in users]
            })
            return HttpResponse(
                json.dumps(data, cls=LazyEncoder),
                content_type='application/json')
        data.update({
            'status': 204,
            'error': _('No users registered as `%(username)s` '
                       'or user is unactived.') % {'username': username}
        })
    else:
        data.update({
            'status': 204,
            'error': _('Validation Failed for field `username`')
        })
    return HttpResponse(
        json.dumps(data, cls=LazyEncoder),
        content_type='application/json')


@login_required
def markdown_image_uploader(request):
    """
    Makdown image upload for locale storage
    and represent as json to markdown editor.
    """
    if request.method == 'POST' and request.is_ajax():
        if 'markdown-image-upload' in request.FILES:
            image = request.FILES['markdown-image-upload']
            image_jpeg_types = [
                'image/jpg', 'image/jpeg', 'image/pjpeg',
            ]
            image_types = [
                'image/png', 'image/gif'
            ]
            image_types.extend(image_jpeg_types)

            if image.content_type not in image_types:
                data = json.dumps({
                    'status': 405,
                    'error': _('Bad image format.')
                }, cls=LazyEncoder)
                return HttpResponse(
                    data, content_type='application/json', status=405)

            if image.size > settings.MAX_IMAGE_UPLOAD_SIZE:
                to_MB = settings.MAX_IMAGE_UPLOAD_SIZE / (1024 * 1024)
                data = json.dumps({
                    'status': 403,
                    'link': '#',
                    'data': {'error': _('Maximum image file is %(size)s MB.') % {'size': to_MB}}
                }, cls=LazyEncoder)
                return HttpResponse(
                    data, content_type='application/json', status=200)

            if image.content_type in image_jpeg_types:
                image = rotate_jpeg_by_exif(image)

            image = scale_down_image(image)

            img_uuid = "{0}-{1}".format(uuid.uuid4().hex[:10], image.name.replace(' ', '-'))
            tmp_file = os.path.join(settings.MARTOR_UPLOAD_PATH, img_uuid)
            def_path = default_storage.save(tmp_file, ContentFile(image.read()))
            img_url = os.path.join(settings.MEDIA_URL, def_path)

            data = json.dumps({
                'status': 200,
                'link': img_url,
                'name': image.name
            })
            return HttpResponse(data, content_type='application/json')
        return HttpResponse(_('Invalid request!'))
    return HttpResponse(_('Invalid request!'))
