"""
Views for file upload API.

This module defines API endpoints for handling
authenticated file uploads using Django REST Framework.
"""

from drf_spectacular.utils import extend_schema

from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import FileSerializer

class UploadFile(APIView):
    """
    API view for handling file uploads.

    Only authenticated users are allowed to upload files.
    """
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=FileSerializer,
        responses={200: str},
    )
    def post(self, request):
        """
        Handle POST request for file upload.

        Args:
            request (Request): The HTTP request containing file data.
            format (str, optional): The format suffix for the request (default: None).

        Returns:
            Response: Success message with HTTP 200 status or
            validation errors with HTTP 400 status.
        """
        
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response("success", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
