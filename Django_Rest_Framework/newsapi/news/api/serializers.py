from datetime import datetime
from django.utils.timesince import timesince
from rest_framework import serializers

from news.models import Article, Journalist


class ArticleSerializer(serializers.ModelSerializer):
    time_since_publication = serializers.SerializerMethodField(method_name="since_publication")
    # author = JournalistSerializer(read_only=True,)
    
    class Meta:
        model = Article
        # fields = "__all__" # we want all the fields of our model to be serialized
        # fields = ("title", "description") # we want only some of fields of our model to be serialized
        exclude = ("id",) # we want to serialize all of fields except "id"

    def since_publication(self, object: Article) -> str: 
        publication_date = object.publication_date
        now = datetime.now()
        time_data = timesince(publication_date, now)
        return time_data
    
    # def get_author(self, object):
    #     author = object.author
    #     # return author.__str__()
    #     return f"{author.first_name} {author.last_name}"
    
    def validate(self, data):
        """check that description and title are different
        Args:
            data (_type_): _description_
        """
        if data["title"] == data["description"]:
            raise serializers.ValidationError("Title and Description must be different from one another.")
        return data
    
    def validate_title(self, value):
        if len(value) < 10:
           raise serializers.ValidationError("Title must be at least 10 characters .") 
        return value + "_validated_"
 
 

class JournalistSerializer(serializers.ModelSerializer):
    articles = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name="article-detail")
    # articles = ArticleSerializer(read_only=True, many=True) # cách 1
    class Meta:
        model = Journalist
        fields = "__all__" # we want all the fields of our model to be serialized
         
# class ArticleSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     author = serializers.CharField()
#     title = serializers.CharField()
#     description = serializers.CharField()
#     body = serializers.CharField()
#     location = serializers.CharField()
#     publication_date = serializers.DateField()
#     active = serializers.BooleanField()
#     created_at = serializers.DateTimeField(read_only=True)
#     updated_at = serializers.DateTimeField(read_only=True)
    
    
#     def create(self, validated_data):
#         print(validated_data)
#         instance = Article.objects.create(**validated_data)
#         return instance
    
#     def update(self, instance, validated_data):
        
#         instance.author = validated_data.get('author', instance.author)
#         instance.title = validated_data.get('author', instance.title)
#         instance.description = validated_data.get('description', instance.description)
#         instance.location = validated_data.get('location', instance.location)
#         instance.publication_date = validated_data.get('publication_date', instance.publication_date)
#         instance.active = validated_data.get('active', instance.active)
#         instance.created_at = validated_data.get('created_at', instance.created_at)
#         instance.updated_at = validated_data.get('updated_at', instance.updated_at)
#         instance.save()
        
#         return instance
        
#     def validate(self, data):
#         """check that description and title are different

#         Args:
#             data (_type_): _description_
#         """
        
#         if data["title"] == data["description"]:
#             raise serializers.ValidationError("Title and Description must be different from one another.")
#         return data
    
#     def validate_title(self, value):
#         if len(value) < 60:
#            raise serializers.ValidationError("Title must be at least 60 characters .") 
#         return value + "_validated_"