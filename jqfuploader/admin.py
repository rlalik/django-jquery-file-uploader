from django.contrib import admin

# Register your models here.
from .models import UploadSettings, UploadFile, DataSet

#from django.db.models.base import ModelBase

class UploadSettingsAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, { 'fields' : [
            'enable_upload', 'max_upload_size',
            'max_chunk_size', 'allowed_types' ]
        }),
    ]

    list_display = [ 'enable_upload', 'max_upload_size',
                    'max_chunk_size', 'allowed_types' ]

class UploadFileAdmin(admin.ModelAdmin):
    #fieldsets = [
        #(None, { 'fields' : [
            #'enable_upload', 'max_upload_size',
            #'max_chunk_size', 'allowed_types' ]
        #}),
    #]

    list_display = [ 'file_name', 'total_size', 'recorded_size',
                    'recorded_md5', 'unique_id' ]

admin.site.register(UploadSettings, UploadSettingsAdmin)
admin.site.register(UploadFile, UploadFileAdmin)
#admin.site.register(DataSet)
