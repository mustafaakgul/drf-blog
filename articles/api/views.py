from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from articles.models import Article
from articles.api.serializers import ArticleSerializer

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from articles.api.permissions import IsOwner
from rest_framework.filters import SearchFilter, OrderingFilter
from articles.api.paginations import PostPagination
from accounts.api.throttles import ArticleListUserThrottle
from accounts.api.throttles import RegisterThrottle
from articles.api.paginations import PostPagination
from articles.api.permissions import IsOwner

from articles.api.serializers import PostSerializer, PostUpdateCreateSerializer
from articles.models import Article
from rest_framework.permissions import (
    IsAuthenticated,
)

from rest_framework.generics import \
    ListAPIView,\
    CreateAPIView,\
    UpdateAPIView, \
    RetrieveAPIView,\
    DestroyAPIView,\
    RetrieveUpdateAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin


class ArticleListAPIView(ListAPIView):
    throttle_classes = [ArticleListUserThrottle]
    queryset = Article.objects.all()
    serializer_class = PostSerializer
    #swagger_schema = ProductXcodeAutoSchema


class PostListAPIViewFilter(ListAPIView, CreateModelMixin):
    # throttle_scope = "hasan"
    serializer_class = PostSerializer
    #searching
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content']  #/list?search=pycharm  pycharmda gore ara
    #ordering ise eklendgnde syledir list?seach=asda&ordering=title   title gre srala
    #pagination
    pagination_class = PostPagination

    #filtreleme
    def get_queryset(self):
        queryset = Post.objects.filter(draft=False)
        return queryset

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)


class PostDetailAPIView(RetrieveAPIView): # inherit ettik
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "slug"  # sluga gore detay syfasina gidilecek id yerine gciyor url den snra
    #defualt olarak lookup field pk dir yani id dir


class PostDetailAPIViewId(RetrieveAPIView): # inherit ettik
    queryset = Article.objects.all()
    serializer_class = PostSerializer
    lookup_field = "pk"


class PostDeleteAPIView(DestroyAPIView): # inherit ettik
    queryset = Article.objects.all()
    serializer_class = PostSerializer
    lookup_field = "slug"
    permission_classes = [IsOwner]


class PostUpdateAPIView(UpdateAPIView): # inherit ettik
    queryset = Article.objects.all()
    serializer_class = PostSerializer
    lookup_field = "slug"

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class PostUpdateAPIView(RetrieveUpdateAPIView, DestroyModelMixin):
    queryset = Article.objects.all()
    serializer_class = PostUpdateCreateSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwner]

    def perform_update(self, serializer):
        serializer.save(modified_by = self.request.user)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class PostCreateAPIView(CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = PostUpdateCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)


"""

class PostUpdateAPIView(RetrieveUpdateAPIView): # bu update den farkı alanlar dolu olarak glir
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    lookup_field = "slug"
    permission_classes = [IsOwner]

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)

#create icine list mixin ekleme
class PostCreateAPIView(CreateAPIView, ListModelMixin): # inherit ettik
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated] #user giris yapmıs ise
    #permission_classes = [IsOwner, IsAdminUser] #burada or yok ikisinide karsılarsa yapar
    #or icin method icinde degisiklk yapılır
    #giris yapldi ise

    def get (self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
        #mail gnderme bradan


"""
class PostCreateAPIView(CreateAPIView): # inherit ettik
    queryset = Article.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated]
    #giris yapldi ise

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
        #mail gnderme bradan


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()


"""
from rest_framework import permissions
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView
)
from articles.models import Article
from .serialzers import ArticleSerializer


class ArticleListView(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (permissions.AllowAny, )


class ArticleDetailView(RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (permissions.AllowAny, )


class ArticleCreateView(CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ArticleUpdateView(UpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ArticleDeleteView(DestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (permissions.IsAuthenticated, )"""

"""
#alttaki save metodu koyarsan kendi save ini override edersn bu calisir digerini ezer ve oncekiler
#olmadngndan calismaz hata verr save yapamaz
def save(self, **kwargs):
    print("save1")
    return True
#save e git 2 tane metod castryor update ve create yoksa create
#SONUC save metodu bizim create mi yoksa update e mi gidicegimizi belirler
#craete yoksa olrstrr update varsa gnceller
"""

# save yerine create kullandm ama kendi create olstrmak istirm djangonnkini dgil
# CREATE METODU
"""
def create(self, validated_data):
    return Post.objects.create(user = self.context["request"].user, **validated_data)
ama kendiside olr tabiki create default olnı kullan yani dgstrmek istrsek byle gibi
"""
# su demek create olstrdm ama user olayini kendm vermek istedm kendimin  verdigi user blgisini klln
# gerisi aynı olsn **validate data geri kalan valide dataları aynn ilet demek
"""
#update ise syle bu sayede veriyede backendden mudahaele erisiblr olacagz
def update(self, instance, validated_data):
    instance.title = validated_data.get("title", instance.title)  # title al yoksa instance title al
    instance.content = "editlendi backend tarfndan"
    instance.save()
    #degerlr buradaki gibi propertileri tek tek alınıp birşeyler yapularblr ve altta herpsi icin bir method
    #cagirilir


def validate_title(self, value):
    if value == "mstafa":
        raise serializers.ValidationError("bu dger olmaz")
    return value
#validate ise attribute bazli calisablr o attribute senaryoda ise bseyler ypıyot yukarda mstafa
#ise olmayacak exception frlatacak

def validate(self, attrs):  #hepsi icin calisir btn attri burada custom valdasyn yapblr ama kendisi yterli olacaktr bence
    print(attrs["title"])
    return attrs
#ornegn bradaki valdayn mstafa grrsen olmayacak gibi
#tek tekmethod yazılablr yada burada butun propertiler print att deki giib cekilip kendi validate yapılblr
"""
"""
shellden girip yapılblr alttada ktuphanede bnları ypıyor
obj = Post.objects.first()
obj.title
new = PostSerializer(obj)  # serialize edildi
new.data["title"]
veri = {"title" : "baslik", "content" : "icerik"}
new = PostSerializer(data=veri) #ekleme islemi ve validationyapar
#validasyon olmadan formlardaki gibi veriyi gnderemeyiz ilk isvalid
if new.is_valid():
    new.save()
else:
    print(new.errors)

shell update delete
python manage.py shell
from post.api.postserializer import postserialzize
from post.model import post
obj = post object get (id=7)
obj.delete ile siler
obj.title
data = {"title" : "yenititle", "content" : "iceirk"}
process = postserializer(obj, data=data)
process.isvalid()
    #edil ypmadan once validmi ona bkmamaz lazm
process.errors
if process.isvalid()
    process.save
"""