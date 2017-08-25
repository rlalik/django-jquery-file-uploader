from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse

from .models import UploadFile

class UploadError(Exception):
    def __init__(self, status=500, **kwargs):
        self.status = status
        self.data = kwargs


class UploadResponse(HttpResponse):
    def __init__(self, content, status=200, *args, **kwargs):
        super(UploadResponse, self).__init__(
            content=DjangoJSONEncoder().encode(content),
            content_type='application/json',
            status=status,
            *args, **kwargs
        )

class UploadFinished(HttpResponse):
    def __init__(self, upload, *args, **kwargs):

        upload_dict = {
            'name' : upload.file_name,
            'size' : upload.recorded_size,
            'url': upload.file.url,
            'thumbnailUrl': upload.file.url,
            'deleteUrl': reverse('jqfuploader:delete', args=(upload.unique_id.hex,)),
            'deleteType': "DELETE"
        }
        res = { 'files' : [ upload_dict] }

        super(UploadFinished, self).__init__(
            content=DjangoJSONEncoder().encode(res),
            content_type='application/json',
            status=200,
            *args, **kwargs
        )
