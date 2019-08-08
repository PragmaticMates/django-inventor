from PIL import Image
from django.core.files.base import ContentFile, File
import hashlib
import os
import six
from django.conf import settings
from django.core.cache import cache
from django.utils.text import slugify
from django.utils.encoding import force_bytes


def avatar_path_handler(instance=None, filename=None, size=None, ext=None):
    tmppath = ['avatars']
    #tmppath.append(force_text(instance.pk))

    if not filename:
        # Filename already stored in database
        filename = instance.avatar.name

    if size:
        tmppath.extend(['resized', str(size)])

    tmppath.append(os.path.basename(filename))
    return os.path.join(*tmppath)


cached_funcs = set()


def get_cache_key(user, size, prefix):
    """
    Returns a cache key consistent of a username and image size.
    """
    key = six.u('%s_%s_%s') % (prefix, user.pk, size)
    return six.u('%s_%s') % (slugify(key)[:100], hashlib.md5(force_bytes(key)).hexdigest())


def cache_result(default_size=settings.AVATAR_DEFAULT_SIZE):
    """
    Decorator to cache the result of functions that take a ``user`` and a
    ``size`` value.
    """
    if not settings.AVATAR_CACHE_ENABLED:
        def decorator(func):
            return func
        return decorator

    def decorator(func):
        def cached_func(user, size=None):
            prefix = func.__name__
            cached_funcs.add(prefix)
            key = get_cache_key(user, size or default_size, prefix=prefix)
            result = cache.get(key)
            if result is None:
                result = func(user, size or default_size)
                cache.set(key, result, settings.AVATAR_CACHE_TIMEOUT)
            return result
        return cached_func
    return decorator


def invalidate_cache(user, size=None):
    """
    Function to be called when saving or changing an user's avatars.
    """
    sizes = set(settings.AVATAR_AUTO_GENERATE_SIZES)
    if size is not None:
        sizes.add(size)
    for prefix in cached_funcs:
        for size in sizes:
            cache.delete(get_cache_key(user, size, prefix))


def avatar_thumbnail_exists(user, size):
    return user.avatar.storage.exists(user.avatar_name(size))


def create_avatar_thumbnail(user, size, quality=None):
    # invalidate the cache of the thumbnail with the given size first
    invalidate_cache(user, size)
    try:
        orig = user.avatar.storage.open(user.avatar.name, 'rb')
        image = Image.open(orig)
        quality = quality or settings.AVATAR_THUMB_QUALITY
        w, h = image.size
        if w != size or h != size:
            if w > h:
                diff = int((w - h) / 2)
                image = image.crop((diff, 0, w - diff, h))
            else:
                diff = int((h - w) / 2)
                image = image.crop((0, diff, w, h - diff))
            if image.mode not in ("RGB", "RGBA"):
                image = image.convert("RGB")
            image = image.resize((size, size), settings.AVATAR_RESIZE_METHOD)
            thumb = six.BytesIO()
            image.save(thumb, settings.AVATAR_THUMB_FORMAT, quality=quality)
            thumb_file = ContentFile(thumb.getvalue())
        else:
            thumb_file = File(orig)
        thumb = user.avatar.storage.save(user.avatar_name(size), thumb_file)
    except IOError:
        return  # What should we do here?  Render a "sorry, didn't work" img?
