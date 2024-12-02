# kakaomap/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import requests

@api_view(['GET'])
def bank_search(request):
    """은행 검색"""
    query = request.GET.get('query', '')
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')

    if not query:
        return Response({'error': '검색어를 입력하세요'}, status=400)

    # 카카오맵 API 호출
    headers = {
        'Authorization': f'KakaoAK {settings.KAKAO_REST_API_KEY}'
    }
    params = {
        'query': query,
        'category_group_code': 'BK9'  # 은행 코드
    }

    if lat and lng:
        params.update({
            'x': lng,
            'y': lat,
            'radius': 5000  # 5km
        })

    try:
        response = requests.get(
            'https://dapi.kakao.com/v2/local/search/keyword.json',
            headers=headers,
            params=params
        )
        return Response(response.json())
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def nearby_banks(request):
    """주변 은행 검색"""
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')

    if not (lat and lng):
        return Response({'error': '위치 정보가 필요합니다'}, status=400)

    headers = {
        'Authorization': f'KakaoAK {settings.KAKAO_REST_API_KEY}'
    }
    params = {
        'category_group_code': 'BK9',
        'x': lng,
        'y': lat,
        'radius': 5000,
        'sort': 'distance'
    }

    try:
        response = requests.get(
            'https://dapi.kakao.com/v2/local/search/category.json',
            headers=headers,
            params=params
        )
        return Response(response.json())
    except Exception as e:
        return Response({'error': str(e)}, status=500)