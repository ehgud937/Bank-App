# products/models.py
from django.db import models


# Create your models here.
class DepositProducts(models.Model):
    fin_prdt_cd = models.TextField(unique=True) # 금융상품코드
    kor_co_nm = models.TextField()              # 금융회사명
    fin_prdt_nm = models.TextField()            # 금융상품명
    etc_note = models.TextField()               # 금융 상품 설명
    join_deny = models.IntegerField()           # 가입제한(1:제한없음, 2:서민전용, 3:일부제한)
    join_member = models.TextField()            # 가입대상
    join_way = models.TextField()               # 가입방법
    spcl_cnd = models.TextField()               # 우대조건

class DepositOptions(models.Model):
    product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE)  # 외래키
    fin_prdt_cd = models.TextField()                                        # 금융 상품 코드
    intr_rate_type_nm = models.CharField(max_length=100)                    # 저축금리 유형명
    intr_rate = models.FloatField(default= -1)                                         # 저축금리
    intr_rate2 = models.FloatField(default= -1)                                        # 최고우대금리
    save_trm = models.IntegerField()                                        # 저축기간(단위: 개월)

class SavingProducts(models.Model):
    fin_prdt_cd = models.TextField(unique=True) # 금융상품코드
    kor_co_nm = models.TextField()              # 금융회사명
    fin_prdt_nm = models.TextField()            # 금융상품명
    etc_note = models.TextField()               # 금융 상품 설명
    join_deny = models.IntegerField()           # 가입제한(1:제한없음, 2:서민전용, 3:일부제한)
    join_member = models.TextField()            # 가입대상
    join_way = models.TextField()               # 가입방법
    spcl_cnd = models.TextField()               # 우대조건   

class SavingOptions(models.Model):
    product = models.ForeignKey(SavingProducts, on_delete=models.CASCADE)  # 외래키
    fin_prdt_cd = models.TextField()                                        # 금융 상품 코드
    intr_rate_type_nm = models.CharField(max_length=100)                    # 저축금리 유형명
    intr_rate = models.FloatField(default= -1)                                         # 저축금리
    intr_rate2 = models.FloatField(default= -1)                                        # 최고우대금리
    save_trm = models.IntegerField() 


class MortgageProducts(models.Model):
    fin_prdt_cd = models.TextField(unique=True) # 금융상품코드
    kor_co_nm = models.TextField()              # 금융회사명
    fin_prdt_nm = models.TextField()            # 금융상품명
    join_way = models.TextField()               # 가입 방법
    loan_inci_expn = models.TextField()         # 대출 부대비용
    erly_rpay_fee = models.TextField()          # 중도상환 수수료
    dly_rate = models.TextField()               # 연체 이자율
    loan_lmt = models.TextField()               # 대출한도

class MortgageOtions(models.Model):
    product = models.ForeignKey(MortgageProducts, on_delete=models.CASCADE)
    fin_prdt_cd = models.TextField() 
    mrtg_type = models.TextField()              # 담보유형 코드
    mrtg_type_nm = models.TextField()           # 담보유형
    rpay_type = models.TextField()              # 대출상환유형 코드
    rpay_type_nm = models.TextField()           # 대출상환유형
    lend_rate_type = models.TextField()         # 대출금리유형 코드
    lend_rate_type_nm = models.TextField()      # 대출금리유형
    lend_rate_min = models.FloatField()         # 대출금리 최저(소수점 2자리)
    lend_rate_max = models.FloatField()         # 대출금리 최고(소수점 2자리)
    lend_rate_avg = models.FloatField()         # 전월 취급 평균금리(소수점 2자리)