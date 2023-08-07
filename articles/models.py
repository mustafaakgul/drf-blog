from django.db import models
from core.models.core import CoreModel
from tags.models import Tag
from django.contrib.auth.models import User


class Article(CoreModel):
    author = models.ForeignKey(User, related_name='articles', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=1000)
    tags = models.ManyToManyField(Tag, related_name='articles', blank=True)
    image = models.ImageField(upload_to='article/', null=True, blank=True)
