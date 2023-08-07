from django.db import models
from core.models.core import CoreModel
from autoslug import AutoSlugField


class Tag(CoreModel): # Category
    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.slug
