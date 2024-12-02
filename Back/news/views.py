# news/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import NewsArticle, NewsKeyword
from .serializers import NewsArticleSerializer, NewsKeywordSerializer
from django.db.models import Q

@api_view(['GET'])
def news_list(request):
    # 검색어 처리
    query = request.GET.get('q', '')
    if query:
        articles = NewsArticle.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )
    else:
        articles = NewsArticle.objects.all()
    
    # 카테고리 필터
    category = request.GET.get('category', '')
    if category:
        articles = articles.filter(category=category)
    
    # 페이지네이션
    page = int(request.GET.get('page', 1))
    size = int(request.GET.get('size', 10))
    start = (page - 1) * size
    end = start + size
    
    serializer = NewsArticleSerializer(
        articles[start:end], 
        many=True
    )
    
    return Response({
        'articles': serializer.data,
        'total': articles.count(),
        'page': page,
        'size': size
    })

@api_view(['GET'])
def trending_keywords(request):
    keywords = NewsKeyword.objects.all()[:10]
    serializer = NewsKeywordSerializer(keywords, many=True)
    return Response(serializer.data)