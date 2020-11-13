from rest_framework import serializers
from news.models import Article
from news.models import Journalist
from django.utils import timezone
class ArticleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    author = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    body = serializers.CharField()
    location = serializers.CharField()
    publication_date = serializers.DateTimeField()
    active = serializers.BooleanField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        print(validated_data)
        return Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.author = validated_data.get('author', instance.author)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.body = validated_data.get('body', instance.body)
        instance.location = validated_data.get('location', instance.location)
        instance.publication_date = validated_data.get('publication_data', instance.publication_date)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance

class JournalistSerializer(serializers.ModelSerializer):

    #articles = ArticleSerializer(many = True, read_only = True)
    
    #links of related object
    #articles = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name="article-detail")
    # HyperlinkedRelatedField는 ForgeignKey로 연결된 타겟 필드의 API url을 리턴
    # many,read_only, view_name을 지정해줘야함 , 특히 view_name은 참조할 api의 url의 name을 명시해야 함
    
    class Meta:
        model = Journalist
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    time_since_publication = serializers.SerializerMethodField()
    #author = serializers.StringRelatedField()
    # ForgeignKey로 연결된 모델의 __str__ 메소드에서 정의한 string을 리턴

    #author = JournalistSerializer(read_only=True)
    # 참조할 모델의 Serializer를 가져와서 사용
    # Journalist <- Article이 정참조하는 관계 (1:N)로서 ArticleSerializer에서 author를 참조할 수 있고 반대로 JournalistSerializer에서 articles를 참조할 수 도 있음

    
    class Meta:
        model = Article
        fields = "__all__"

    def get_time_since_publication(self,object):
        publication_date = object.publication_date
        now = datetime.now(timezone.utc)
        time_delta = timesince(publication_date,now)
        return time_delta 