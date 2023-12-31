from django.db import models


class TimeStampModel(models.Model):
    """Abstract model to add created_at and updated_at fields to models"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
