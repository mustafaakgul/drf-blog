from django.db import models
from core.models.core import CoreModel
from tags.models import Tag
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone


class Article(CoreModel):
    author = models.ForeignKey(User, related_name='articles', on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=150, editable=False)  #sluglarn unique olmasi cok onmli id gibi olmali
    # slug = AutoSlugField(populate_from='title', unique=True)

    content = models.TextField(max_length=1000)
    draft = models.BooleanField(default=False) #taslaklara kydetmek icin

    tags = models.ManyToManyField(Tag, related_name='articles', blank=True) # Categories
    image = models.ImageField(upload_to='articles/', null=True, blank=True)

    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="modified")
    # burada set null ise user slinirse dataya bsey olmaz modified by slnmez yani slnrse null olsn

    class Meta:
        ordering = ['-id']
        # verbose_name = 'Article'
        # verbose_name_plural = 'Articles'
        # db_table = 'Article'

    def __str__(self):
        return self.title

    def get_slug(self):  #editable yapınca buradan dzenlneblir demek
        slug = slugify(self.title.replace("ı","i"))
        unique = slug
        number = 1

        while Article.objects.filter(slug = unique).exists():
            unique = '{}-{}'.format(slug, number)
            number += 1

        return unique

    def save(self, *args, **kwargs):
        if not self.id:  # ilk olstugunda id olmayacagndan sadece ilkinde girecek
            self.created = timezone.now()
        self.modified = timezone.now()
        self.slug = self.get_slug()
        return super(Article, self).save(*args, **kwargs)
