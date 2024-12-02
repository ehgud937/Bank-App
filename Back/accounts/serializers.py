# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer
import uuid
User = get_user_model()

# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer

User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(required=True)  # username 직접 입력 받음
    email = serializers.EmailField(required=True)
    birthdate = serializers.DateField(required=True)
    assets = serializers.IntegerField(required=True, min_value=0)
    annual_income = serializers.IntegerField(required=True, min_value=0)
    investment_type = serializers.ChoiceField(
        choices=User.INVESTMENT_TYPE_CHOICES,
        required=True
    )
    primary_bank = serializers.ChoiceField(
        choices=User.BANK_CHOICES,
        required=True
    )

    def validate_username(self, username):
        # username 중복 체크
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("이미 사용중인 아이디입니다.")
        return username

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update({
            'username': self.validated_data.get('username'),  # 직접 입력받은 username
            'email': self.validated_data.get('email'),
            'birthdate': self.validated_data.get('birthdate'),
            'assets': self.validated_data.get('assets'),
            'annual_income': self.validated_data.get('annual_income'),
            'investment_type': self.validated_data.get('investment_type'),
            'primary_bank': self.validated_data.get('primary_bank'),
        })
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'birthdate', 'assets', 'annual_income', 
                 'investment_type', 'primary_bank')
        read_only_fields = ('email',)

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'birthdate', 'assets', 'annual_income', 
                 'investment_type', 'primary_bank')
        read_only_fields = ('email', 'id')

from dj_rest_auth.serializers import LoginSerializer

class CustomLoginSerializer(LoginSerializer):
    username = None  # username 필드 제거
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):
       # email을 authentication을 위한 identify로 사용
       email = attrs.get('email')
       if email:
           user = User.objects.filter(email=email).first()
           if user:
               attrs['username'] = user.username
       return super().validate(attrs)
    

class AdditionalUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['birthdate', 'assets', 'annual_income', 'investment_type', 'primary_bank']



class DeleteAccountSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True)

    def validate_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        return value