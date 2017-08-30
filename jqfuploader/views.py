# -*- encoding: utf-8 -*-
import re

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.core.files.base import ContentFile
from django.views.generic import View, TemplateView

from .models import DataSet, UploadFile, UploadSettings
from .responses import UploadResponse, UploadError, UploadFinished

# Create your views here.
def index(request):
    try:
        set = UploadSettings.objects.get(enable_upload=True)
    except UploadSettings.DoesNotExist:
        return HttpResponse('Sorry, no upload allowed. <a href="/">Go to the main page</a>')
    except UploadSettings.MultipleObjectsReturned:
        setlist = UploadSettings.objects.filter(enable_upload=True)
        set = setlist[0];

    context = { 'settings' : set }
    return render(
        request,
        'jqfuploader/index.html',
        context
    )

class UploadBaseView(View):
    model = UploadFile
    field_name = 'files'
    content_range_header = 'HTTP_CONTENT_RANGE'
    content_range_pattern = re.compile(
        r'^bytes (?P<start>\d+)-(?P<end>\d+)/(?P<total>\d+)$'
    )

    def get_content_range(self, request, chunk):
        content_range = request.META.get(self.content_range_header)
        if content_range is not None:
            match = self.content_range_pattern.match(content_range)
            if match:
                start = int(match.group('start'))
                end = int(match.group('end'))
                total = int(match.group('total'))
            else:
                raise UploadError(message='The Content Range header seems wrong.', status=400)
            if end - start + 1 != chunk.size:
                raise UploadFile(message='The chunk size don\'t match the header.', status=400)
        else:
            start = 0
            end = chunk.size - 1
            total = chunk.size
        return start, end, total

    @staticmethod
    def get_or_create_dataset(name):
        try:
            dataset = DataSet.objects.get(name=name)
        except DataSet.DoesNotExist:
            dataset = DataSet(name=name)
            dataset.save()
        return dataset

    def get_or_create_chunked_upload(self, name, total_size, dataset):
        try:
            chunked_upload = self.model.objects.get(file_name=name, total_size=total_size, dataset=dataset)
        except self.model.DoesNotExist:
            empty_chunk = ContentFile(name=name, content='')
            chunked_upload = self.model(file=empty_chunk, file_name=name, total_size=total_size, dataset=dataset)
            chunked_upload.recorded_md5 = 0;
            chunked_upload.recorded_size = 0;
            chunked_upload.save()
        except self.model.MultipleObjectsReturned:
            chunked_uploads = self.model.objects.filter(file_name=chunk.name, total_size=total_size, dataset=dataset)
            map(lambda x: x.delete(), chunked_uploads[1:])
            chunked_upload = chunked_uploads[0]
        return chunked_upload

    def _post(self, request):
        raise NotImplementedError("You have to define this method in children View class")

    def post(self, request):
        try:
            return self._post(request)
        except UploadError as error:
            return UploadResponse(error.data, status=error.status)
        except Exception as error:
            return UploadResponse({'message': error.__str__()}, status=500)

class UploadView(UploadBaseView):
    def _post(self, request):
        chunk = request.FILES.get(self.field_name)
        start, end, total = self.get_content_range(request, chunk)
        file_name = chunk._get_name();
        dataset_name = request.POST.get('dataset_name')
        if dataset_name == None:
            dataset_name = "dsname_%s" % re.sub('[.\ ]', '_', file_name)
        dataset = self.get_or_create_dataset(dataset_name)
        chunked_upload = self.get_or_create_chunked_upload(chunk.name, total, dataset)
        if chunked_upload.is_finished:
            return UploadFinished(chunked_upload)
        else:
            if start == 0:
                chunked_upload.append_chunk(chunk, mode='wb')
            else:
                if chunked_upload.current_size == start:
                    chunked_upload.append_chunk(chunk)
                else:
                    raise UploadError(
                        message='Upload content\'s start don\'t '
                                'equal to the file current size',
                        status=400
                    )
            chunked_upload.save()

        if chunked_upload.is_finished:
            chunked_upload.recorded_md5 = chunked_upload.md5
            return UploadFinished(chunked_upload)

        return UploadFinished(chunked_upload)
        #return UploadResponse({'status': 'success'}, status=202)

def delete(request, uid):
        try:
            file = UploadFile.objects.get(unique_id=uid)
            file.delete_file()
            file.delete()
        except UploadFile.DoesNotExist:
            pass

        return UploadResponse({'status': 'success'}, status=202)
