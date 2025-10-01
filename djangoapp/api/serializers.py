"""
Serializers for file upload API.

This module defines serializers used for handling
file uploads via the Django REST Framework.
"""

from rest_framework import serializers
from api.models import Document

import uuid

class FileSerializer(serializers.Serializer):
    """
    Serializer for handling file uploads.

    Attributes:
        file (FileField): The uploaded file to be processed.
    """
    file = serializers.FileField()

    def create(self, validated_data):
        """
        Create and return a new `Document` instance, given the validated data.
        """
        user = self.context['request'].user
        return Document.objects.create(title=validated_data['file'].name, file=validated_data['file'], user=user)
    
    def update(self, instance, validated_data):
        """
        Update and return an existing `Document` instance, given the validated data.
        """
        pass

class DocumentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Document model, exposing id, title, and file fields.
    """
    class Meta:
        model = Document
        fields = ['ids', 'title', 'file']

class ChatInputSerializer(serializers.Serializer):
    """
    Serializer for validating chat input data.

    This serializer validates the incoming data for the chat API, ensuring that:
    - A valid UUID is provided for `document_id`.
    - At least one of `text` or `audio` is provided (audio file or non-empty text).
    - `text` is optional but if provided can be blank.
    - `audio` is optional and can be null.

    Fields:
        document_id (UUIDField): The UUID of the document to interact with.
        text (CharField): Optional user text input; can be blank.
        audio (FileField): Optional audio file input; can be null.

    Methods:
        validate(attrs):
            Custom validation to ensure either audio or non-empty text is present.

    Raises:
        serializers.ValidationError: If both audio and non-empty text are missing.
    """
    document_id = serializers.UUIDField()
    text = serializers.CharField(required=False, allow_blank=True)
    audio = serializers.FileField(required=False, allow_null=True)

    def validate(self, attrs):
        text = attrs.get('text')
        audio = attrs.get('audio')

        if not audio and (not text or text.strip() == ''):
            raise serializers.ValidationError("Either audio file or non-empty text must be provided.")

        return attrs
