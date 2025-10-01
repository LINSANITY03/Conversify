"""
Django model definition for Document.

This module defines the Document model, which represents
a file-based resource stored in the system with metadata.
"""

import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Document(models.Model):
    """
    Represents a document uploaded to the system.

    Attributes:
        id (UUID): Primary key, auto-generated UUID for the document.
        title (str): The title of the document, limited to 200 characters.
        file (FileField): File associated with the document, stored under 'Documents/'.
        created_at (datetime): Timestamp when the document was created.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, help_text="Unique identifier for the document.")
    user= models.ForeignKey(User, related_name='document', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=False)
    file = models.FileField(upload_to='Documents', null=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """
        Return a string representation of the document.

        Returns:
            str: The UUID and title of the document.
        """
        return f"{self.id} {self.title}"