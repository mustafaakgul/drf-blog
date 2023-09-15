from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from articles.models import Article

#parent bir yorum oteknin altina atlablr ondan kllncaz kendisine gibi

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name="comments")
    post = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    created = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Comment, self).save(*args,**kwargs)

    def __str__(self):
        return f"{self.post.title} {self.user.username}"

    def children(self):
        return Comment.objects.filter(parent = self)  #bana ait yrmlar
    @property
    def any_children(self):
        return Comment.objects.filter(parent = self).exists()  # bana yrm varmi, bnm atlmda yrm varmı

    class Meta:
        ordering = ("created",)
        # db_table = 'yorum'
        # verbose_name = 'Yorum'
        # verbose_name_plural = 'Yorumlar'
