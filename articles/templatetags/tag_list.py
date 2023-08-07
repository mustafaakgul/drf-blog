from django import template
from tags.models import Tag


register = template.Library()


@register.simple_tag
def tag_list():
    return Tag.objects.all()
