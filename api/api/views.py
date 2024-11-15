from django.core.files import File
from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser, JSONParser
from os import remove
from os.path import splitext, basename
from .models import Document
from .serializer import DocumentUpdateSerializer, DocumentUploadSerializer, DocumentsUploadSerializer
from .constants import file_path
from .validators import validate_unique_file_name_for_user
from rest_framework import views

# Create your views here.

@api_view(['GET'])
@parser_classes([MultiPartParser, FormParser])
def get_docs(request):
    docs = Document.objects.all()
    serializer = DocumentUploadSerializer(docs, many=True)
    for i in range(len(docs)):
        serializer.data[i]['nameOfFile'] = basename(docs[i].fileUrl.path)    
    serializedData = serializer.data
    return Response(serializedData)


@api_view(['POST'])
@parser_classes([MultiPartParser, FileUploadParser])
def add_docs(request):
    data = request.data
    serializer = DocumentUploadSerializer(data=data)
    print('hi')
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    

@api_view(['POST'])
@parser_classes([JSONParser, MultiPartParser])
def update_doc(request, pk):
    document_for_update = Document.objects.get(pk = pk) 
    data = request.data
    print(document_for_update.fileUrl.path)
    try: 
        old_file_path = document_for_update.fileUrl.path
        old_file_name, old_file_ext = splitext(old_file_path)
        validate_unique_file_name_for_user(data['fileName']+old_file_ext)
        

        with open(old_file_path, "rb") as old_file:
            updated_file = File(old_file)
            document_for_update.fileUrl.save(data['fileName']+old_file_ext, updated_file)
    
        remove(old_file_path)
    
        serializer = DocumentUpdateSerializer(instance = document_for_update, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except ValidationError:
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['DELETE'])
def delete_doc(request, pk):
    try:
        document_for_deletion = Document.objects.get(pk = pk) 
        remove(document_for_deletion.fileUrl.path)
        document_for_deletion.delete()
        return Response(status=status.HTTP_200_OK)
    except Document.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
from rest_framework import generics
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from .constants import allowed_files


class FileDownloadListAPIView(generics.ListAPIView):

    def get(self, request, pk, format=allowed_files):
        queryset = Document.objects.get(pk=pk)
        file_handle = queryset.fileUrl.path
        ext = splitext(file_handle)[1]
        file_content_type = format[ext]
        document = open(file_handle, 'rb')
        response = HttpResponse(FileWrapper(document), content_type=file_content_type)
        response['Content-Disposition'] = 'attachment; filename="%s"' % queryset.fileUrl.name
        return response