# recommendations/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .services import FinancialRecommender
from .serializers import RecommendationSerializer
from .models import ProductRecommendation

# recommendations/views.py
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommendations(request):
    try:
        recommender = FinancialRecommender(request.user)
        recommendations = recommender.get_recommendations()
        
        # 이전 추천 결과 삭제
        ProductRecommendation.objects.filter(user=request.user).delete()
        
        response_data = {
            'rule_based': {
                'title': '맞춤형 금융 상품 추천',
                'description': '고객님의 투자성향과 자산을 고려한 추천입니다.',
                'products': _format_rule_based_recommendations(
                    recommendations['rule_based'], 
                    'RULE_BASED',
                    request.user
                )
            },
            'ml_based': {
                'title': '사용자 정보 기반 추천',
                'description': '비슷한 프로필의 고객님들이 선택한 상품입니다.',
                'products': _format_ml_based_recommendations(
                    recommendations['ml_based'],
                    'ML_BASED',
                    request.user
                )
            }
        }
        
        return Response(response_data)
        
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

def _format_rule_based_recommendations(recommendations, rec_type, user):
    """규칙 기반 추천 결과 포맷팅"""
    formatted_data = {}
    
    for product_type, products_dict in recommendations.items():
        formatted_data[product_type] = []
        
        for category, products in products_dict.items():
            for rank, product in enumerate(products, 1):
                recommendation = ProductRecommendation.objects.create(
                    user=user,
                    product_type=product_type.upper(),
                    recommendation_type=category,
                    rank=rank,
                    confidence_score=0.8
                )
                
                if product_type == 'deposit':
                    recommendation.deposit_product = product
                elif product_type == 'saving':
                    recommendation.saving_product = product
                elif product_type == 'mortgage':
                    recommendation.mortgage_product = product
                    
                recommendation.save()
                
                serializer = RecommendationSerializer(recommendation)
                formatted_data[product_type].append(serializer.data)
    
    return formatted_data

def _format_ml_based_recommendations(recommendations, rec_type, user):
    """ML 기반 추천 결과 포맷팅"""
    formatted_data = {}
    
    for product_type, products in recommendations.items():
        formatted_data[product_type] = []
        
        for rank, product in enumerate(products, 1):
            recommendation = ProductRecommendation.objects.create(
                user=user,
                product_type=product_type.upper(),
                recommendation_type=rec_type,
                rank=rank,
                confidence_score=0.8
            )
            
            if product_type == 'deposit':
                recommendation.deposit_product = product
            elif product_type == 'saving':
                recommendation.saving_product = product
            elif product_type == 'mortgage':
                recommendation.mortgage_product = product
                
            recommendation.save()
            
            serializer = RecommendationSerializer(recommendation)
            formatted_data[product_type].append(serializer.data)
    
    return formatted_data