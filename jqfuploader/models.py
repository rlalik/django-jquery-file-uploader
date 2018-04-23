import hashlib
import os
import uuid

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_delete

def generate_file_path(instance, filename):
    return os.path.join(instance.dataset.name, filename)

class UploadFileBase(models.Model):
    file = models.FileField(blank=True, upload_to=generate_file_path)
    file_name = models.CharField(max_length=255)
    total_size = models.BigIntegerField(default=0)
    recorded_size = models.BigIntegerField(default=0)
    recorded_md5 = models.CharField(max_length=32, blank=True)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False)

    @property
    def current_size(self):
        return self.file.size

    @property
    def md5(self):
        md5 = hashlib.md5()
        close_after = False

        if self.file.closed:
            self.file.open('rb')
            close_after = True

        for chunk in self.file.chunks():
            md5.update(chunk)

        if close_after:
            self.close_file()

        return md5.hexdigest()

    @property
    def is_finished(self):
        return self.total_size == self.recorded_size

    class Meta:
        abstract = True
        unique_together = (('file_name', 'total_size'),)

    def __str__(self):
        return 'name: {file_name}; size: {total_size}; md5: {recorded_md5}; uid: {unique_id}'.format(
            file_name=self.file_name,
            total_size=self.total_size,
            recorded_md5=self.recorded_md5,
            unique_id=self.unique_id
        )

    def close_file(self):
        """
        Bug in django 1.4: FieldFile `close` method is not reaching all the
        way to the actual python file.
        Fix: we had to loop all inner files and close them manually.
        """
        file_ = self.file
        while file_ is not None:
            file_.close()
            file_ = getattr(file_, 'file', None)

    def delete_file(self):
        print('removing ' + self.file.path)
        os.remove(self.file.path)

    def append_chunk(self, chunk, mode='ab'):
        self.close_file()
        self.file.open(mode=mode)
        self.file.write(chunk.read())
        self.recorded_size = self.current_size
        self.close_file()

class DataSet(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class UploadFile(UploadFileBase):
    dataset = models.ForeignKey(DataSet)

    class Meta:
        unique_together = (('dataset', 'unique_id'), ('dataset', 'file_name', 'total_size'))

# These two auto-delete files from filesystem when they are unneeded:
@receiver(post_delete, sender=UploadFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `UploadFileBase` object is deleted.
    """
    print('removing ' + instance.file.path)
    if instance.file:
        os.remove(instance.file.path)

class UploadSettings(models.Model):
    enable_upload = models.BooleanField(default=True)
    max_upload_size = models.IntegerField(default=999000000)
    max_chunk_size = models.IntegerField(default=1000000)
    allowed_types = models.TextField(default='/(\.|\/)(gif|jpe?g|png|mp4)$/i')
    page_title = models.CharField(max_length=100, default="jQuery File Upload")
    page_notes = models.TextField(),
    notification_email = models.TextField(),
