"""
Used for registered model for common apps.
from django.db import models
"""
from django.db import models


class TimeStampedModel(models.Model):
    """
    An abstract model that provides fields for tracking creation and update times.

    Fields:
        created_at (datetime): The datetime when the object was created.
        updated_at (datetime): The datetime when the object was last updated.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta for TimeStampedModel Model
        """
        abstract = True
