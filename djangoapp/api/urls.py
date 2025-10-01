"""
URL configuration for the API.

This module defines the URL routes for file upload
and authentication endpoints.
"""

from django.urls import path, include

from api import views

urlpatterns = [
    path("upload/", views.UploadFile.as_view(), name="file-upload"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
