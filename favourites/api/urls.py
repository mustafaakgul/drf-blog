from django.urls import path, include
from django.urls import path
from comment.api.views import *
from .views import *


app_name = "favourites"


urlpatterns = [
    # path('create', CommentCreateAPIView.as_view(), name='create'),
    path('list-create', FavouriteListCreateAPIView.as_view(), name='list-create'),
    # path('listcomment', CommentList4CommentAPIView.as_view(), name='listcomment'),
    # path('delete/<pk>', CommentDeleteAPIView.as_view(), name='delete'),
    path('update-delete/<pk>', FavouriteAPIView.as_view(), name='update-delete'),
]