# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class User(AbstractUser):
    BANK_CHOICES = [
        ('KB', 'KB국민은행'),
        ('SH', '신한은행'),
        ('WR', '우리은행'),
        ('NH', '농협은행'),
        ('IBK', '기업은행'),
        ('KEB', '하나은행'),
        ('ETC', '기타'),
    ]
    
    INVESTMENT_TYPE_CHOICES = [
        ('CONSERVATIVE', '안정형'),
        ('MODERATE', '중립형'),
        ('AGGRESSIVE', '공격형'),
        ('SPECULATIVE', '위험추구형'),
    ]

    email = models.EmailField(unique=True, verbose_name='이메일')
    username = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='아이디'
    )
    birthdate = models.DateField(null=True, verbose_name='생년월일')
    assets = models.BigIntegerField(
        validators=[MinValueValidator(0)],
        default=0,
        verbose_name='보유자산',
        help_text='단위: 원'
    )
    annual_income = models.BigIntegerField(
        validators=[MinValueValidator(0)],
        default=0,
        verbose_name='연봉',
        help_text='단위: 원'
    )
    investment_type = models.CharField(
        max_length=20,
        choices=INVESTMENT_TYPE_CHOICES,
        default='MODERATE',
        verbose_name='투자성향'
    )
    primary_bank = models.CharField(
        max_length=10,
        choices=BANK_CHOICES,
        default='ETC',
        verbose_name='주거래은행'
    )

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = '사용자 목록'
        ordering = ['-date_joined']

    def __str__(self):
        return self.email

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)