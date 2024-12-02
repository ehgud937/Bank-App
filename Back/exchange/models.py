# exchange/models.py
from django.db import models

# Create your models here.
class ExchangeRate(models.Model):
    cur_unit = models.CharField(max_length=20)              # 통화코드 (USD, JPY 등)
    cur_nm = models.CharField(max_length=20)                # 국가/통화명 (미국 달러, 일본 엔 등)
    ttb = models.FloatField(null=True)                      # 전신환(송금) 받으실때
    tts = models.FloatField(null=True)                      # 전신환(송금) 보내실때
    deal_bas_r = models.FloatField()                        # 매매 기준율
    bkpr = models.IntegerField(null=True)                   # 장부가격
    yy_efee_r = models.FloatField(null=True)               # 년환가료율
    ten_dd_efee_r = models.FloatField(null=True)           # 10일환가료율
    kftc_deal_bas_r = models.FloatField(null=True)         # 서울외국환중개 매매기준율
    kftc_bkpr = models.IntegerField(null=True)             # 서울외국환중개 장부가격
    update_date = models.DateField()                        # 환율 고시 날짜
    
    class Meta:
        ordering = ['-update_date']                         # 최신 날짜순으로 정렬
        indexes = [
            models.Index(fields=['cur_unit']),              # 통화 코드 검색 최적화
            models.Index(fields=['update_date']),           # 날짜 검색 최적화
        ]
        constraints = [
            models.UniqueConstraint(                        # 같은 날짜에 같은 통화는 하나만
                fields=['cur_unit', 'update_date'],
                name='unique_currency_date'
            )
        ]

    def __str__(self):
        return f"[{self.update_date}] {self.cur_nm}({self.cur_unit}): {self.deal_bas_r}"