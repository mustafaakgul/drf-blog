from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers

from comment.models import Comment
from post.models import Post

class CommentCreateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['created',]

    def validate(self, attrs):
        if(attrs["parent"]):  #parenti varsa
            if attrs["parent"].post != attrs["post"]:  #paarentinın post u ile post aynı olmalı
                raise serializers.ValidationError("something went wrong")
        return attrs
    #parentı yoksa olusturur yada parent varsa esitlk saglanmalı yoksa baskas postun yorumunun altına girer
"""
class CommentChildSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class CommentListSerializer(ModelSerializer):
    replies = SerializerMethodField()
    class Meta:
        model = Comment
        fields = '__all__'

    def get_replies(self, obj):
        if obj.any_children:
            return CommentChildSerializer(obj.children(), many  =True).data

"""

"""
all list
class CommentListSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
"""

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "id"]

class PostCommentSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "slug", "id"]

class CommentListSerializer(ModelSerializer):
    replies = SerializerMethodField()  # json icine yeni alan eklemek
    user = UserSerializer()
    post = PostCommentSerializer()
    class Meta:
        model = Comment
        fields = '__all__'

    def get_replies(self, obj):
        if obj.any_children:  #burası bir properrty onceden olusturuldu fonk gibi cagırılmaz o yuzden bunu olusturrken property olduguun syleriz
            return CommentListSerializer(obj.children(), many  =True).data  #recursive ile dndurduk


"""
class CommentListSerializer(ModelSerializer):
    replies = SerializerMethodField()
    class Meta:
        model = Comment
        fields = '__all__'
        depth = 1 # icinde alnlarn nesne varsa id yerine nesneyi detaylı acar

    def get_replies(self, obj):
        if obj.any_children:
            return CommentListSerializer(obj.children(), many  =True).data

"""

class CommentDeleteUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["content"]