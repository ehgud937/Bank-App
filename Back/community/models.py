# community/models.py
from django.db import models
from django.conf import settings
# Create your models here.

class Article(models.Model):
    CATEGORY_CHOICES = [
        ('FREE', '자유'),
        ('ASK', '질문'),
        ('REVIEW', '후기'),
        ('ETC', '기타'),
        ('NOTIFICATION', '공지'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(
        max_length=15,
        choices=CATEGORY_CHOICES,
        default='FREE',
        verbose_name='질문카테고리'
    )
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles')

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']