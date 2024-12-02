# accounts/urls.py

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/update/', views.UserProfileUpdateView.as_view(), name='profile_update'),
    path('kakao/login/', views.kakao_login, name='kakao_login'),
    path('kakao/callback/', views.kakao_callback, name='kakao_callback'),
    path('additional-info/', views.additional_info, name='additional_info'),
    path('check-additional-info/', views.check_additional_info, name='check_additional_info'),
    path('delete/', views.DeleteAccountView.as_view(), name='delete_account'),
]