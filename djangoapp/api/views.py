"""
Views for file upload API.

This module defines API endpoints for handling
authenticated file uploads using Django REST Framework.
"""

from drf_spectacular.utils import extend_schema

from rest_framework import status, permissions
from rest_framework.generics import RetrieveAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import FileSerializer, DocumentSerializer, ChatInputSerializer
from api.models import Document

import os
import requests

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
    lookup_field = 'id'

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
            document = Document.objects.get(id=serializer.validated_data['document_id'])
        except Document.DoesNotExist:
            return Response({"error": "Document not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user != document.user:
            return Response({"error": "User not matched."}, status=status.HTTP_401_UNAUTHORIZED)
        
        # user_audio = serializer.validated_data.get('audio')
        user_text = serializer.validated_data.get('text')
        # Prioritize audio: transcribe if audio present
        
        # Prepare payload for n8n webhook
        payload = {
            "document_url": document.file.url,
            "user_query": user_text,
        }
        
        try:
            resp = requests.post(os.getenv('PIPELINE_URL'), json=payload)
            resp.raise_for_status()
        except requests.RequestException as e:
            return Response({"error": f"Failed to send data to n8n: {str(e)}"}, status=status.HTTP_502_BAD_GATEWAY)

        # Optionally return whatever n8n returns
        return Response({"n8n_response": resp.json()})
