# Back/urls.py
from django.contrib import admin
from django.urls import path, include
from dj_rest_auth.registration.views import (
    SocialLoginView, 
    SocialAccountListView
)
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

class KakaoLogin(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter
    callback_url = "http://localhost:8000/accounts/kakao/callback/"  # 콜백 URL 수정
    client_class = OAuth2Client

from django.http import JsonResponse
def home(request):
    return JsonResponse({
        "message": "Welcome to the API",
        "endpoints": {
            "admin": "/admin/",
            "kakao_login": "/accounts/kakao/login/",
            "api": "/api/v1/",
        }
    })

urlpatterns = [
    # Admin
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    
    # Authentication URLs
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/signup/', include('dj_rest_auth.registration.urls')),
    
    # Social Authentication
    path('accounts/kakao/login/', include('allauth.socialaccount.providers.kakao.urls')),  # 이 줄 추가
    path('accounts/social/kakao/', KakaoLogin.as_view(), name='kakao_login'),
    path('accounts/social/connections/', SocialAccountListView.as_view(), name='social_account_list'),
    
    # allauth URLs
    path('accounts/', include('allauth.urls')),  # 이 줄 추가
    
    # API URLs
    path('api/v1/', include([
        path('accounts/', include('accounts.urls')),
    ])),

    # product app
    path('products/', include('products.urls')),

    # exchange app
    path('exchange/', include('exchange.urls')),
    
    # kakaomap app
    path('api/v1/kakaomap/', include('kakaomap.urls')),

    # community app
    path('community/', include('community.urls')),

    # recommend app
    path('recommend/', include('recommend.urls')),

    # news app
    path('news/', include('news.urls')),

    # register app
    path('register/', include('register.urls')),

    # chat app
    path('chat/', include('chat.urls'))
]
# 디버그 모드에서 DRF 브라우저블 API 활성화
from django.conf import settings
if settings.DEBUG:
    urlpatterns += [
        path('api-auth/', include('rest_framework.urls')),
    ]