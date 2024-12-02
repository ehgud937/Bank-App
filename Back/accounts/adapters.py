# accounts/adapters.py
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_field
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        email = data.get('email')
        username = data.get('username')  # 직접 입력받은 username
        
        # email과 username 모두 설정
        user_field(user, 'email', email)
        user_field(user, 'username', username)
        
        if 'password1' in data:
            user.set_password(data['password1'])
        else:
            user.set_unusable_password()
            
        user.birthdate = data.get('birthdate')
        user.assets = data.get('assets', 0)
        user.annual_income = data.get('annual_income', 0)
        user.investment_type = data.get('investment_type', 'MODERATE')
        user.primary_bank = data.get('primary_bank', 'ETC')
        
        if commit:
            user.save()
        return user
    
class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        
        # 고유한 username 생성
        uid = uuid.uuid4().hex[:10]
        username = f"kakao_{uid}"
        while User.objects.filter(username=username).exists():
            uid = uuid.uuid4().hex[:10]
            username = f"kakao_{uid}"
        
        user.username = username
        
        # email이 없는 경우 임시 이메일 생성
        if not user.email:
            user.email = f"{username}@example.com"
            
        return user

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        
        # 여기서 추가 필드 설정 가능
        if sociallogin.account.provider == 'kakao':
            user.save()
        
        return user