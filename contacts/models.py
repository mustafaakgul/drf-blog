from django.db import models
from core.models.core import CoreModel


class Contact(CoreModel):
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    message = models.TextField(max_length=500)

    def __str__(self):
        return f"{self.email} - {self.full_name}"
