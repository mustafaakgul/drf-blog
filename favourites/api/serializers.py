from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from favourite.models import Favourite

class FavouriteListCreateAPISerializer(ModelSerializer):
    class Meta:
        model = Favourite
        fields = "__all__"

    def validate(self, attrs):
        print(attrs["post"])
        print(attrs["user"])
        queryset = Favourite.objects.filter(post = attrs["post"], uesr = attrs["user"])
        if queryset.exists():  #bu sunu yapacak daha once favorilere eklendyse bi daha eklenmesn diye ckarr
            raise serializers.ValidationError("already added")

        return attrs
    #bu validate bu sey favorilere eklendiyse bir daha eklenmesn demek zaten favorilere ekledn


class FavouriteAPISerializer(ModelSerializer):
    class Meta:
        model = Favourite
        fields = ('content',)