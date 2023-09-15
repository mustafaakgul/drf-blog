from django.contrib import admin
from articles.models import Article


# admin.site.register(Article)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('author', 'title',)
    search_fields = ('title',)
