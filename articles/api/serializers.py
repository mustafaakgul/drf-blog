from rest_framework import serializers
from articles.models import Article


"""
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'email', 'first_name', 'last_name',)
"""


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article

        fields = [
            "title",
            "content",
            "image",
        ]

    """
    burada save update create override edersek orjinallarndekiler calısmaz burada kendileri calısır
    save bir işlem icin ilk yapılan ordan update veya create gitmesi gerektigine bakıp ilgili yere gidiyor
    """


class PostSerializer(serializers.ModelSerializer):
    # Old Method
    # title = serializers.CharField(max_length=200)  # formlarda oldugu gibi tanmlanablr
    # # form dada form.charfield vardı
    # content = serializers.CharField(max_length=200)

    #tags = TagSerializer(many=True, required=False, read_only=True)
    #author = UserSerializer(required=False, read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='articles:detail',
        lookup_field='slug' # sluga gore islemleri ypmak url de slug oldgndan
    )

    # alttaki ile user1 yerine ismini yazmak icin
    username = serializers.SerializerMethodField(method_name="get_username") # bununla get_username yada alttak kllnlablr

    class Meta:
        model = Article

        fields = [
            'pk',
            'username', # old is 'user'
            'title',
            'content',
            'tags',
            'author',
            'image',
            'url', # slug yerine url yazldi
            'created_at',
            'updated_at',
            'modified_by'
        ]

    def get_username(self, obj):
        return str(obj.user.username)

    """
        def save(self, **kwargs):
            print("test")
            return 1
        this save method is overrided and if we use this save instead of original save that is stated in
        drf source, this method just show print("test") not any saving process and controls.
        to use custom permission methods override it with all body or empty, and write smt
        """

class PostUpdateCreateSerializer(serializers.ModelSerializer):
   class Meta:
       model = Article
       fields = [
           'title',
           'content',
           'image',
       ]