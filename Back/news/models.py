# news/models.py
from django.db import models

class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    url = models.URLField()
    press = models.CharField(max_length=50)  # 언론사
    published_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=50)  # 뉴스 카테고리 (증권, 금융 등)
    thumbnail_url = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['category']),
        ]

class NewsKeyword(models.Model):
    keyword = models.CharField(max_length=50, unique=True)
    count = models.IntegerField(default=0)  # 키워드 출현 빈도
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-count']