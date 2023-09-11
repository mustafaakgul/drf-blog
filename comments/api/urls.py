from django.urls import path, include

from django.urls import path
from comment.api.views import *
app_name = "comment"
urlpatterns = [
    path('create', CommentCreateAPIView.as_view(), name='create'),
    path('list', CommentListAPIView.as_view(), name='list'),
    path('listcomment', CommentList4CommentAPIView.as_view(), name='listcomment'),
    path('delete/<pk>', CommentDeleteAPIView.as_view(), name='delete'),
    path('update/<pk>', CommentUpdateAPIView.as_view(), name='update'),
]
