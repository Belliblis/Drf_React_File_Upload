from django.core.exceptions import ValidationError
from os.path import splitext, exists, abspath
from .constants import valid_extensions

def validate_file_extension(value):
    ext = splitext(value.name)[1]  # [0] returns path+filename
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')
    
def validate_file_size(value): 
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MB.')
    
def validate_unique_file_name_for_user(value):
    filename = abspath("media/uploads/"+value)
    if exists(filename):
        raise ValidationError("File with this name already exists. Please provide unique name.")