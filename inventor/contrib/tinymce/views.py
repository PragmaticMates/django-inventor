import os
from uuid import uuid4

from django.conf import settings
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def upload_file_to_folder(request, *args, **kwargs):
    if request.method != "POST":
        return JsonResponse({"Error Message": "Wrong request"})

    file_obj = request.FILES["file"]
    file_name_suffix = file_obj.name.split(".")[-1]

    file_path = os.path.join(settings.MEDIA_ROOT, "uploads", file_obj.name)

    if os.path.exists(file_path):
        file_obj.name = str(uuid4()) + "." + file_name_suffix
        file_path = os.path.join(settings.MEDIA_ROOT, "uploads", file_obj.name)

    with open(file_path, "wb+") as f:
        for chunk in file_obj.chunks():
            f.write(chunk)

        return JsonResponse(
            {
                "message": "File uploaded successfully",
                "location": os.path.join(settings.MEDIA_URL, "uploads", file_obj.name),
            }
        )


@csrf_exempt
def upload_file_to_bucket(request, *args, **kwargs):
    if request.method != "POST":
        return JsonResponse({"Error Message": "Wrong request"})

    file = request.FILES.get("file")
    file_path = f"tinymce/{uuid4()}/{file.name}"

    # print(default_storage.bucket)
    # print(default_storage.url(file_path, expire=1))

    with default_storage.open(file_path, "wb") as f:
        for chunk in file.chunks():
            f.write(chunk)

    return JsonResponse(
        {
            "message": "File uploaded successfully",
            "location": f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{file_path}",
        }
    )
