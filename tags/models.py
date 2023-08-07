from django.db import models
from core.models.core import CoreModel


class Tag(CoreModel):
    name = models.CharField(max_length=100, unique=True)
