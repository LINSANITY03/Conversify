"""
Serializers for file upload API.

This module defines serializers used for handling
file uploads via the Django REST Framework.
"""

from rest_framework import serializers
from api.models import Document

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