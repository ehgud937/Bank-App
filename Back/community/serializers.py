# community/serializers.py
from rest_framework import serializers
from .models import Article, Comment
from django.contrib.auth import get_user_model

class ArticleListSerializer(serializers.ModelSerializer):
   username = serializers.CharField(source='user.username', read_only=True)
   like_count = serializers.IntegerField(source='like_users.count', read_only=True)
   
   class Meta:
       model = Article
       fields = ('id', 'title', 'username', 'category', 'created_at', 'like_count')

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'content', 'username', 'created_at', 'updated_at')
        read_only_fields = ('user', 'article')

class ArticleSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user', 'like_users')
