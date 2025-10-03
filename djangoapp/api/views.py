"""
Views for file upload API.

This module defines API endpoints for handling
authenticated file uploads using Django REST Framework.
"""
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import FileResponse
from drf_spectacular.utils import extend_schema

from rest_framework import status, permissions
from rest_framework.generics import RetrieveAPIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import FileSerializer, DocumentSerializer, ChatInputSerializer
from api.models import Document

import os
import requests
import uuid

from dotenv import load_dotenv

load_dotenv()

class UploadFile(APIView):
    """
    API view for handling file uploads.

    Only authenticated users are allowed to upload files.
    """
    parser_classes = (MultiPartParser, FormParser)
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

class DocumentDetail(RetrieveAPIView):
    """
    RetrieveAPIView for fetching a single Document instance
    belonging to the authenticated user.
    """

    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'ids'

    def get_queryset(self):
        """
        Returns a queryset of Document instances
        that belong to the currently authenticated user.

        Returns:
            QuerySet: Filtered Document queryset
        """
        return Document.objects.filter(user=self.request.user)

class ChatWithDocument(APIView):
    """
    API view to handle chat interactions with a document.

    This view accepts POST requests containing a document ID and a user query (text or audio),
    validates the input, verifies user authorization against the document owner,
    and sends the query along with the document URL to an external n8n workflow via a webhook.

    Attributes:
        parser_classes (tuple): Parsers to handle multipart/form-data and form data.
        serializer_class (Serializer): Serializer class used to validate incoming data.
        permission_classes (list): List of permission classes; requires authenticated users.

    Methods:
        post(request):
            Handles POST requests with document ID and user query,
            validates data, checks user permissions, sends data to n8n,
            and returns the response from n8n or error messages.
    """

    parser_classes = (MultiPartParser, FormParser)
    serializer_class = ChatInputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            document = Document.objects.get(ids=serializer.validated_data['document_id'])
        except Document.DoesNotExist:
            return Response({"error": "Document not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user != document.user:
            return Response({"error": "User not matched."}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_audio = serializer.validated_data.get('audio')

        if user_audio:
            # Generate a unique filename to avoid collisions
            ext = os.path.splitext(user_audio.name)[1]  # e.g. ".mp3"
            unique_filename = f"{uuid.uuid4().hex}{ext}"

            # Save file to MEDIA_ROOT/uploads/
            default_storage.save(
                os.path.join('uploads', unique_filename),
                user_audio
            )

            # Prepare payload for n8n webhook   
            payload = {
                "document_url": document.file.url,
                "user_query": unique_filename,
            }
        
        try:
            resp = requests.post(os.getenv('PIPELINE_URL'), json=payload)
            resp.raise_for_status()
        except requests.RequestException as e:
            return Response({"error": f"Failed to send data to n8n: {str(e)}"}, status=status.HTTP_502_BAD_GATEWAY)

        # Optionally return whatever n8n returns
        return Response({"n8n_response": resp.json()})

class StreamAudioFromUrl(APIView):
    """
    API view to stream an audio file from the server's media storage.

    This view handles GET requests and streams the requested audio file
    if it exists in the 'uploads' directory under MEDIA_ROOT. If the file
    does not exist, it returns a 404 error response.

    Attributes:
        permission_classes (list): Permissions allowed for this view (AllowAny).
        serializer_class: Not used in this view (set to None).
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = None

    def get(self, request, filename):
        """
        Handles GET requests to stream an audio file by filename.

        Args:
            request (Request): The HTTP request object.
            filename (str): The name of the audio file to stream.

        Returns:
            FileResponse: Streaming response containing the audio file with MIME type 'audio/mpeg',
                          if the file exists.
            Response: JSON error response with status 404 if the file is not found.
        """
        
        # Construct full file path
        audio_url = os.path.join(settings.MEDIA_ROOT, 'uploads', filename)

        if not os.path.exists(audio_url):
            return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)

        # Stream the file
        return FileResponse(open(audio_url, 'rb'), content_type='audio/mpeg')