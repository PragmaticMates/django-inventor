import io
from io import BytesIO
from PIL import Image, ExifTags
from django.core.files.base import File


def scale_down_image(image, base_size=1024):
    pil_image = Image.open(io.BytesIO(image.read()))
    image_format = pil_image.format
    image.seek(0)

    if pil_image.size[0] > base_size or pil_image.size[1] > base_size:
        ratio = (base_size / float(pil_image.size[0])) if pil_image.size[0] > pil_image.size[1] else (base_size / float(pil_image.size[1]))
        y_size = int((float(pil_image.size[1]) * float(ratio)))
        x_size = int((float(pil_image.size[0]) * float(ratio)))
        pil_image = pil_image.resize((x_size, y_size), Image.ANTIALIAS)
        output = BytesIO()
        pil_image.save(output, format=image_format)
        output.seek(0)
        image = File(output, image.name)
    return image


def rotate_jpeg_by_exif(image):
    pil_image = Image.open(BytesIO(image.read()))
    image.seek(0)

    for orientation_key in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation_key] == 'Orientation':
            break

    exif = pil_image._getexif()
    if exif is None:
        return image

    exif_items = dict(exif.items())
    exif_orientation = exif_items.get(orientation_key, None)

    if exif_orientation is not None:
        if exif_orientation == 3:
            pil_image = pil_image.rotate(180, expand=True)
        elif exif_orientation == 6:
            pil_image = pil_image.rotate(270, expand=True)
        elif exif_orientation == 8:
            pil_image = pil_image.rotate(90, expand=True)

        output = BytesIO()
        pil_image.save(output, format='JPEG', quality=75)
        output.seek(0)
        image = File(output, image.name)

    return image
