from rest_framework import serializers
from .models import Document
from .constants import valid_extensions
from os.path import splitext
class DocumentUploadSerializer(serializers.ModelSerializer):

    
    fileId = serializers.CharField(required = False)
    fileName = serializers.CharField(required = False)
    fileUrl = serializers.FileField(required = True)

    class Meta:
        model = Document
        fields = "__all__"


class DocumentUpdateSerializer(serializers.ModelSerializer):

    fileId = serializers.CharField(required = False)
    
    class Meta:
        model = Document
        fields = "__all__"
        extra_kwargs = {
            'id': {'read_only': True},
            'fileUrl': {'read_only': True}
        }
    def validate_format(self, fileUrl):
        if splitext(fileUrl.name)[1]not in valid_extensions: 
            raise serializers.ValidationError('Wrong ext')
        return fileUrl
    

class DocumentsUploadSerializer(serializers.Serializer):
    files = serializers.ListField(child = serializers.FileField(write_only= True))


    

    