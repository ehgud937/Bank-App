# accounts/views.py

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, AdditionalUserInfoSerializer, UserUpdateSerializer, DeleteAccountSerializer
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
import requests
from recommend.models import ProductRecommendation

User = get_user_model()

BASE_URL = 'http://localhost:5173/'  # 프론트엔드 URL
KAKAO_CALLBACK_URI = BASE_URL + 'accounts/kakao/callback'

class UserProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class UserProfileUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerializer

    def get_object(self):
        return self.request.user

@api_view(['GET'])
def kakao_login(request):
    client_id = settings.SOCIALACCOUNT_PROVIDERS['kakao']['APP']['client_id']
    return Response({
        'kakao_login_url': f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code"
    })

@api_view(['GET'])
def kakao_callback(request):
    code = request.GET.get("code")
    CLIENT_ID = settings.KAKAO_REST_API_KEY
    REDIRECT_URI = 'http://localhost:5173/accounts/kakao/callback'

    # 카카오 토큰 받기
    token_req = requests.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&code={code}"
    )
    access_token = token_req.json().get('access_token')
    
    # 카카오 사용자 정보 가져오기
    profile_req = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    profile_json = profile_req.json()
    
    # 프로필에서 닉네임 가져오기
    nickname = profile_json.get('properties', {}).get('nickname')
    
    # 닉네임으로 사용자 생성 또는 로그인
    user, created = User.objects.get_or_create(
        username=nickname,
        defaults={'email': f"{nickname}@kakao.user"}  # 임시 이메일 생성
    )
    
    # 토큰 발급
    token, _ = Token.objects.get_or_create(user=user)
    
    response_data = {
        "key": token.key,
        "nickname": nickname,
        "needs_additional_info": created
    }
    
    return Response(response_data)

class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def additional_info(request):
    serializer = AdditionalUserInfoSerializer(data=request.data, instance=request.user)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_additional_info(request):
    user = request.user
    needs_info = any([
        user.birthdate is None,
        user.assets == 0,
        user.annual_income == 0,
        user.investment_type == 'MODERATE',
        user.primary_bank == 'ETC'
    ])
    return Response({"needs_additional_info": needs_info})

# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeleteAccountSerializer 

    def delete(self, request):
        serializer = DeleteAccountSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            user = request.user
            # 연관된 데이터 삭제 또는 처리
            try:
                # 토큰 삭제
                Token.objects.filter(user=user).delete()
                
                # 사용자가 작성한 게시글, 댓글 등 처리
                user.article_set.all().delete()  # CASCADE 설정에 따라 댓글도 자동 삭제
                
                # 가입 상품 정보 처리
                user.deposit_registers.all().delete()
                user.saving_registers.all().delete()
                user.mortgage_registers.all().delete()
                
                # 채팅 기록 삭제
                user.conversation_set.all().delete()
                
                # 추천 정보 삭제
                ProductRecommendation.objects.filter(user=user).delete()
                
                # 사용자 삭제
                user.delete()
                
                return Response(
                    {"message": "계정이 성공적으로 삭제되었습니다."},
                    status=status.HTTP_204_NO_CONTENT
                )
            except Exception as e:
                return Response(
                    {"error": "계정 삭제 중 오류가 발생했습니다."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)