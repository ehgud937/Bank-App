# community/views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Article, Comment
from .serializers import ArticleListSerializer, ArticleSerializer, CommentSerializer
from rest_framework import status

# Create your views here.
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def article_list_create(request):
    print('tt')
    if request.method == 'GET':
        articles = Article.objects.all()
        serializers = ArticleListSerializer(articles, many=True)
        return Response(serializers.data)
    
    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data)
        
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def article_detail(request, article_pk):
   article = get_object_or_404(Article, pk=article_pk)
   
   if request.method == 'GET':
       serializer = ArticleSerializer(article)
       return Response(serializer.data)
   
   # 자신의 게시글만 수정/삭제 가능
   if request.user != article.user:
       return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
       
   if request.method == 'PUT':
       serializer = ArticleSerializer(article, data=request.data)
       if serializer.is_valid(raise_exception=True):
           serializer.save()
           return Response(serializer.data)
           
   elif request.method == 'DELETE':
       article.delete()
       return Response({'message': '게시글이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def article_like(request, article_pk):
   article = get_object_or_404(Article, pk=article_pk)
   
   # 이미 추천한 경우 추천 취소
   if article.like_users.filter(pk=request.user.pk).exists():
       article.like_users.remove(request.user)
       liked = False
   # 추천하지 않은 경우 추천
   else:
       article.like_users.add(request.user)
       liked = True
       
   return Response({
       'liked': liked,
       'count': article.like_users.count()
   })


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def comment_list_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    if request.method == 'GET':
        comments = article.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(
                user=request.user,
                article=article
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_detail(request, article_pk, comment_pk):
    article = get_object_or_404(Article, pk=article_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)

    # 자신의 댓글만 수정/삭제 가능
    if request.user != comment.user:
        return Response({'error': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
            
    elif request.method == 'DELETE':
        comment.delete()
        return Response({'message': '댓글이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)