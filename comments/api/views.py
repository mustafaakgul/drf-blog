from rest_framework.generics import \
    ListAPIView,\
    CreateAPIView,\
    UpdateAPIView, \
    RetrieveAPIView,\
    DestroyAPIView,\
    RetrieveUpdateAPIView
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from comments.api.pagination import CommentPagination
from comments.models import Comment
from comments.api.serializers import *
from comments.api.permissions import IsOwner


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)


#bu normal bütün commentleri getiri api/comment/list?q=12
# get queryparam -> 12. post a ait yorumlar
class CommentListAPIView(ListAPIView):
    serializer_class = CommentListSerializer
    pagination_class = CommentPagination

    def get_queryset(self):
        queryset = Comment.objects.filter(parent = None)
        query = self.request.GET.get("q")  #sonuna q koyma q yakalamak icin
        if query:
            queryset = queryset.filter(post = query)
        return queryset


class CommentList4CommentAPIView(ListAPIView):
    serializer_class = CommentListSerializer
    pagination_class = CommentPagination
    def get_queryset(self):
        queryset = Comment.objects.filter(parent = None)
        query = self.request.GET.get("q")   #?q=5 yaznca demek http://127.0.0.1:8000/api/comment/listcomment?q=10 JOIN ASLNDA
        if query:  #extra bir quer varsa sayfaya basılanı degistir
            queryset = queryset.filter(post = query)

        return queryset


class CommentDeleteAPIView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDeleteUpdateSerializer
    lookup_field = "pk"
    permission_classes = [IsOwner]


"""
#update and delete class modal mixin http://127.0.0.1:8000/api/comment/delete/8
class CommentDeleteAPIView(DestroyAPIView, UpdateModelMixin, RetrieveModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentDeleteUpdateSerializer
    lookup_field = "pk"
    permission_classes = [IsOwner]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def get(self, request, *args, **kwargs): #retrieve icin cnku retrivvevede gelmesi get ile olr
        return self.retrieve(request, *args, **kwargs)
        
        
class CommentDeleteAPIView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDeleteUpdateSerializer
    lookup_field = "pk"
    permission_classes = [IsOwner]
"""
#buradaki ise update delete fonk eklendi alttaki delete metod ve mixin giris yeterli
class CommentUpdateAPIView(UpdateAPIView, RetrieveAPIView, DestroyModelMixin):  #retrieveapi yada updateapi icin bos dolu
    queryset = Comment.objects.all()
    serializer_class = CommentDeleteUpdateSerializer
    lookup_field = "pk"
    permission_classes = [IsOwner]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)