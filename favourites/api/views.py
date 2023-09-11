from rest_framework.generics import \
    ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from comment.api.serializers import *
from favourites.api.permissions import IsOwner
from favourite.models import Favourite
from favourites.api.serializers import *
from favourites.api.pagination import FavouritePagination


#hem listeleme hem create model mixin blndran bir modeldr 2 mixin var
# bu sayede haricin eklemek yerine mixin ile ugrasmaktansa brden cok
#yapı aynı syfada istiyrsan bnlar mntkli cnku cok ugrasmıyorsn kendi fonksiynlaryla
#dgerlernde asagıya bide fonksiyonlarını yazıodn mixin lerde
class FavouriteListCreateAPIView(ListCreateAPIView):
    #queryset = Favourite.objects.all()
    serializer_class = FavouriteListCreateAPISerializer
    permission_classes = [IsAuthenticated]
    pagination_class = FavouritePagination

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    def get_queryset(self):
        return Favourite.objects.filter(user = self.request.user)


class FavouriteAPIView(RetrieveUpdateDestroyAPIView): #retrieve getrdi update ile update
    queryset = Favourite.objects.all()
    serializer_class = FavouriteAPISerializer
    lookup_field = "pk"
    permission_classes = [IsOwner]

class FavouriteListCreateAPIView(ListCreateAPIView):
    #queryset = Favourite.objects.all()
    serializer_class = FavouriteListCreateAPISerializer
    permission_classes = [IsAuthenticated]
    pagination_class = FavouritePagination

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    def get_queryset(self):
        return Favourite.objects.filter(user = self.request.user)