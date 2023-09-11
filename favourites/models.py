from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from articles.models import Article


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    post = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.user.username} {self.post.title}"