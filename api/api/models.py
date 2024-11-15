from django.db import models
from os import path
from os.path import basename
from uuid import uuid4

from django.core.files.storage import FileSystemStorage
from .validators import validate_file_extension, validate_file_size

class MyFileStorage(FileSystemStorage):

    def get_available_name(self, name, max_length = ...):
        return super().get_available_name(name, max_length)

def get_uuid():
    return str(uuid4())[:10]

# Create your models here.
class Document(models.Model):
    fileName = models.CharField(max_length=255)
    fileId = models.CharField(max_length=10, primary_key=True, default=get_uuid)
    fileUrl = models.FileField(upload_to='uploads/', validators=[validate_file_extension, validate_file_size],storage=MyFileStorage(), null=True)
    
    def __str__(self):
        return basename(self.fileUrl.path)