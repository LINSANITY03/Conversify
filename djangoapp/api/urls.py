"""
URL configuration for the API.

This module defines the URL routes for file upload
and authentication endpoints.
"""

from django.urls import path, include

from api import views

urlpatterns = [
    path("upload/", views.UploadFile.as_view(), name="file-upload"),
    path('documents/<uuid:ids>', views.DocumentDetail.as_view(), name='document-detail'),
    path('chat/', views.ChatWithDocument.as_view(), name="chat-with-document"),
    path('audio_stream/<str:filename>', views.StreamAudioFromUrl.as_view(), name='stream-audio'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
