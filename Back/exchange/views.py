from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import requests
from datetime import datetime, timedelta
from .models import ExchangeRate
from .serializers import ExchangeRateSerialzier
from django.core.cache import cache
from django.utils import timezone
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ExchangeRateService:
   def __init__(self):
       self.api_key = settings.API_KEY2
       self.base_url = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON'

   def get_latest_business_date(self):
       today = datetime.now()
       current_time = today.time()
       
       if current_time.hour < 11:
           today -= timedelta(days=1)
       
       while today.weekday() in [5, 6]:
           today -= timedelta(days=1)
       
       return today.strftime('%Y%m%d')

   def fetch_exchange_rates(self, search_date):
       """API로부터 환율 데이터 조회"""
       url = f'{self.base_url}?authkey={self.api_key}&searchdate={search_date}&data=AP01'
       
       try:
           response = requests.get(url, verify=False, timeout=10)
           if not response.ok:
               print(f"API request failed: {response.status_code}")
               return None
           return response.json()
       except Exception as e:
           print(f"Error fetching data: {e}")
           return None

   def save_rates(self, data, update_date):
       """환율 데이터 저장"""
       saved_count = 0
       errors = []
       
       # 기존 데이터 삭제
       ExchangeRate.objects.filter(update_date=update_date).delete()
       
       for rate in data:
           try:
               ExchangeRate.objects.create(
                   cur_unit=rate['cur_unit'],
                   cur_nm=rate['cur_nm'],
                   ttb=float(rate['ttb'].replace(',', '')) if rate['ttb'] else None,
                   tts=float(rate['tts'].replace(',', '')) if rate['tts'] else None,
                   deal_bas_r=float(rate['deal_bas_r'].replace(',', '')),
                   bkpr=int(rate['bkpr'].replace(',', '')) if rate['bkpr'] else None,
                   yy_efee_r=float(rate['yy_efee_r']) if rate['yy_efee_r'] else 0.0,
                   ten_dd_efee_r=float(rate['ten_dd_efee_r']) if rate['ten_dd_efee_r'] else 0.0,
                   kftc_deal_bas_r=float(rate['kftc_deal_bas_r'].replace(',', '')) if rate['kftc_deal_bas_r'] else None,
                   kftc_bkpr=int(rate['kftc_bkpr'].replace(',', '')) if rate['kftc_bkpr'] else None,
                   update_date=update_date
               )
               saved_count += 1
               
           except Exception as e:
               errors.append({
                   'currency': rate.get('cur_unit'),
                   'error': str(e)
               })
               
       return saved_count, errors

   def get_latest_rates(self):
       """최신 환율 데이터 조회 (캐시 적용)"""
       cache_key = f"exchange_rates_{timezone.now().strftime('%Y%m%d')}"
       cached_data = cache.get(cache_key)
       
       if cached_data:
           return cached_data
           
       search_date = self.get_latest_business_date()
       data = self.fetch_exchange_rates(search_date)
       retries = 0
       
       while not data and retries < 5:
           retries += 1
           search_date = (datetime.strptime(search_date, '%Y%m%d') - timedelta(days=1)).strftime('%Y%m%d')
           data = self.fetch_exchange_rates(search_date)
           
       if not data:
           return None
           
       update_date = datetime.strptime(search_date, '%Y%m%d').date()
       saved_count, errors = self.save_rates(data, update_date)
       
       rates = ExchangeRate.objects.filter(update_date=update_date)
       if rates.exists():
           serialized_data = ExchangeRateSerialzier(rates, many=True).data
           cache.set(cache_key, serialized_data, 60 * 30)  # 30분 캐시
           return serialized_data
           
       return None

exchange_service = ExchangeRateService()

@api_view(['GET'])
def index(request):
   """API로부터 직접 환율 정보 조회"""
   data = exchange_service.fetch_exchange_rates(exchange_service.get_latest_business_date())
   if not data:
       return Response({'error': 'Failed to fetch exchange rates'}, 
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   return Response(data)

@api_view(['GET'])
def save_exchange(request):
   """환율 정보 저장 및 조회"""
   try:
       rates = exchange_service.get_latest_rates()
       if not rates:
           return Response({'error': 'Failed to fetch or save exchange rates'}, 
                         status=status.HTTP_500_INTERNAL_SERVER_ERROR)
       return Response(rates)
   except Exception as e:
       return Response({'error': str(e)}, 
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def exchange_get_all(request):
   """전체 환율 정보 조회"""
   product = get_list_or_404(ExchangeRate)
   if request.method == 'GET':
       serializer = ExchangeRateSerialzier(product, many=True)
       return Response(serializer.data)

@api_view(['GET'])
def exchange_detail(request, currency):
   """특정 통화의 환율 정보 조회"""
   try:
       rates = exchange_service.get_latest_rates()
       if not rates:
           return Response({'error': 'No exchange rate data found'}, 
                         status=status.HTTP_404_NOT_FOUND)
           
       # 특정 통화 필터링
       currency_rate = next((rate for rate in rates if rate['cur_unit'] == currency.upper()), None)
       if not currency_rate:
           return Response({'error': 'Currency not found'}, 
                         status=status.HTTP_404_NOT_FOUND)
           
       return Response(currency_rate)
       
   except Exception as e:
       return Response({'error': str(e)}, 
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)