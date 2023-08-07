from django.db import models


class CoreModel(models.Model):
    """
    Abstract model that defines fields that are used in every model
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
