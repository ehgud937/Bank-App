# kakaomap/models.py
from django.db import models

class BankStore(models.Model):
    bank_name = models.CharField(max_length=100)  # 은행명
    branch_name = models.CharField(max_length=100) # 지점명
    address = models.CharField(max_length=200) # 주소
    tel = models.CharField(max_length=20, null=True) # 전화번호
    lat = models.FloatField() # 위도
    lng = models.FloatField() # 경도
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

