# news/serializers.py
from rest_framework import serializers
from .models import NewsArticle, NewsKeyword

class NewsArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsArticle
        fields = '__all__'

class NewsKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsKeyword
        fields = '__all__'