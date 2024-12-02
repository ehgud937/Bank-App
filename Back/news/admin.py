# news/admin.py
from django.contrib import admin
from .models import NewsArticle, NewsKeyword

admin.site.register(NewsArticle)
admin.site.register(NewsKeyword)