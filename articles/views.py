from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

#from django_blog.apps.blog.models import Post
#from django_blog.apps.blog.rest_api.serializers.post import PostSerializer
from .models import *
from .serializers import *


#post = Post.objects.create(title='First post', text='This is a first post')
#print(PostSerializer(post).data)
# {'pk': '4670511f-4a03-455e-a160-18c396fa743d', 'title': 'First post', 'text': 'This is a first post', 'tags': [], 'author': None, 'image': None}


from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class PostListCreateAPIView(ListCreateAPIView):
    """
    API view to retrieve list of posts or create new
    """
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class PostDetailsAPIView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete post
    """
    serializer_class = PostSerializer
    queryset = Post.objects.get_queryset()