from django.urls import path
from .views import get_docs, add_docs, delete_doc, update_doc, FileDownloadListAPIView

urlpatterns = [
    path('docs/', get_docs, name="get_books"),
    path('docs/add/', add_docs, name="add_doc"),
    path('docs/delete/<str:pk>', delete_doc, name = "delete_doc"),
    path('docs/update/<str:pk>', update_doc, name = "update_doc"),
    path('docs/download/<str:pk>/', FileDownloadListAPIView.as_view(), name="download"),
]
