from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import requests
from .models import DepositOptions, DepositProducts, SavingOptions, SavingProducts, MortgageOtions, MortgageProducts
from .serializers import (DepositOptionsSerializer, DepositProductsSerializer, SavingOptionsSerializer, 
                          SavingProductsSerializer, MortgageOptionsSerializer, MortgageProductsSerializer,
                          DepositProductWithOptionSerialzier, SavingProductWithOptionSerialzier, MortgageProductWithOptionSerialzier)
from django.http import JsonResponse
# Create your views here.

@api_view(['GET'])
def index(request):
    api_key = settings.API_KEY
    api_url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'
    response = requests.get(api_url).json()
    
    return Response(response)

@api_view(['GET'])
def save_deposit_product(request):
    api_key = settings.API_KEY
    api_url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'
    response = requests.get(api_url).json()
    # print(response.get('result').get('baseList'))
    
    for li in response.get('result').get('baseList'):
        fin_prdt_cd = li.get('fin_prdt_cd')
        kor_co_nm = li.get('kor_co_nm')
        fin_prdt_nm = li.get('fin_prdt_nm')
        etc_note = li.get('etc_note')
        join_deny = li.get('join_deny')
        join_member = li.get('join_member')
        join_way = li.get('join_way')
        spcl_cnd = li.get('spcl_cnd')

        if DepositProducts.objects.filter(fin_prdt_cd = fin_prdt_cd).exists():
            continue

        save_data = {
            'fin_prdt_cd' : fin_prdt_cd, 
            'kor_co_nm' : kor_co_nm,
            'fin_prdt_nm' : fin_prdt_nm, 
            'etc_note' : etc_note,
            'join_deny' : join_deny,
            'join_member' : join_member,
            'join_way' : join_way,
            'spcl_cnd' : spcl_cnd
        }

        serializer = DepositProductsSerializer(data=save_data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

    for li in response.get('result').get('optionList'):
        fin_prdt_cd = li.get('fin_prdt_cd')
        intr_rate_type_nm = li.get('intr_rate_type_nm')
        if li.get('intr_rate') == None:
            intr_rate = -1
        else :
            intr_rate = li.get('intr_rate')

        if li.get('intr_rate2') == None:
            intr_rate2 = -1
        else :
            intr_rate2 = li.get('intr_rate2')

        save_trm = li.get('save_trm')

        if DepositOptions.objects.filter(fin_prdt_cd = fin_prdt_cd, intr_rate_type_nm=intr_rate_type_nm, save_trm=save_trm).exists():
            continue

        save_data = {
            'fin_prdt_cd' : fin_prdt_cd,
            'intr_rate_type_nm' : intr_rate_type_nm,
            'intr_rate' : intr_rate,
            'intr_rate2' : intr_rate2,
            'save_trm' : save_trm
        }

        serializer = DepositOptionsSerializer(data=save_data)

        product = DepositProducts.objects.get(fin_prdt_cd = fin_prdt_cd)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save(product = product)

    return JsonResponse({ 'message' : 'data save success'})

@api_view(['GET','POST'])
def deposit_products(request):
    if request.method == 'GET':
        datas = DepositProducts.objects.all()
        serializer = DepositProductsSerializer(datas, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = DepositProductsSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

@api_view(['GET'])
def deposit_product_options(request, fin_prdt_cd):
    data = DepositOptions.objects.filter(fin_prdt_cd = fin_prdt_cd)
    serializer = DepositOptionsSerializer(data, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def top_rate(request):
    product_option = DepositOptions.objects.all().order_by('-intr_rate')[0]
    serializer2 = DepositOptionsSerializer(product_option)
    print(serializer2.data)
    product = DepositProducts.objects.get(fin_prdt_cd = serializer2.data['fin_prdt_cd'])
    serializer = DepositProductsSerializer(product)
    return Response(serializer.data)

@api_view(['GET'])
def index_saving(request):
    api_key = settings.API_KEY
    api_url = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'
    response = requests.get(api_url).json()
    
    return Response(response)


# 적금 상품 db 저장
@api_view(['GET'])
def save_saving_product(request):
    api_key = settings.API_KEY
    api_url = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'
    response = requests.get(api_url).json()
    # print(response.get('result').get('baseList'))
    
    for li in response.get('result').get('baseList'):
        fin_prdt_cd = li.get('fin_prdt_cd')
        kor_co_nm = li.get('kor_co_nm')
        fin_prdt_nm = li.get('fin_prdt_nm')
        etc_note = li.get('etc_note')
        join_deny = li.get('join_deny')
        join_member = li.get('join_member')
        join_way = li.get('join_way')
        spcl_cnd = li.get('spcl_cnd')

        if SavingProducts.objects.filter(fin_prdt_cd = fin_prdt_cd).exists():
            continue

        save_data = {
            'fin_prdt_cd' : fin_prdt_cd, 
            'kor_co_nm' : kor_co_nm,
            'fin_prdt_nm' : fin_prdt_nm, 
            'etc_note' : etc_note,
            'join_deny' : join_deny,
            'join_member' : join_member,
            'join_way' : join_way,
            'spcl_cnd' : spcl_cnd
        }

        serializer = SavingProductsSerializer(data=save_data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

    for li in response.get('result').get('optionList'):
        fin_prdt_cd = li.get('fin_prdt_cd')
        intr_rate_type_nm = li.get('intr_rate_type_nm')
        if li.get('intr_rate') == None:
            intr_rate = -1
        else :
            intr_rate = li.get('intr_rate')

        if li.get('intr_rate2') == None:
            intr_rate2 = -1
        else :
            intr_rate2 = li.get('intr_rate2')

        save_trm = li.get('save_trm')

        if SavingOptions.objects.filter(fin_prdt_cd = fin_prdt_cd, intr_rate_type_nm=intr_rate_type_nm, save_trm=save_trm).exists():
            continue

        save_data = {
            'fin_prdt_cd' : fin_prdt_cd,
            'intr_rate_type_nm' : intr_rate_type_nm,
            'intr_rate' : intr_rate,
            'intr_rate2' : intr_rate2,
            'save_trm' : save_trm
        }

        serializer = SavingOptionsSerializer(data=save_data)

        product = SavingProducts.objects.get(fin_prdt_cd = fin_prdt_cd)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save(product = product)

    return JsonResponse({ 'message' : 'data save success'})


@api_view(['GET'])
def index_mortgage(request):
    api_key = settings.API_KEY
    api_url = f'http://finlife.fss.or.kr/finlifeapi/mortgageLoanProductsSearch.json?auth={api_key}&topFinGrpNo=050000&pageNo=1'
    response = requests.get(api_url).json()
    
    return Response(response)

@api_view(['GET'])
def save_mortgage_product(request):
    api_key = settings.API_KEY
    api_url = f'http://finlife.fss.or.kr/finlifeapi/mortgageLoanProductsSearch.json?auth={api_key}&topFinGrpNo=050000&pageNo=1'
    response = requests.get(api_url).json()

    # baseList 처리
    for li in response.get('result').get('baseList'):
        fin_prdt_cd = li.get('fin_prdt_cd')
        kor_co_nm = li.get('kor_co_nm')
        fin_prdt_nm = li.get('fin_prdt_nm')
        join_way = li.get('join_way')
        loan_inci_expn = li.get('loan_inci_expn')
        erly_rpay_fee = li.get('erly_rpay_fee')
        dly_rate = li.get('dly_rate')
        loan_lmt = li.get('loan_lmt')

        # 이미 존재하는 상품이면 건너뛰기
        if MortgageProducts.objects.filter(fin_prdt_cd=fin_prdt_cd).exists():
            continue

        save_data = {
            'fin_prdt_cd': fin_prdt_cd,
            'kor_co_nm': kor_co_nm,
            'fin_prdt_nm': fin_prdt_nm,
            'join_way': join_way,
            'loan_inci_expn': loan_inci_expn,
            'erly_rpay_fee': erly_rpay_fee,
            'dly_rate': dly_rate,
            'loan_lmt': loan_lmt
        }

        serializer = MortgageProductsSerializer(data=save_data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

    # optionList 처리
    for li in response.get('result').get('optionList'):
        fin_prdt_cd = li.get('fin_prdt_cd')
        mrtg_type = li.get('mrtg_type')
        mrtg_type_nm = li.get('mrtg_type_nm')
        rpay_type = li.get('rpay_type')
        rpay_type_nm = li.get('rpay_type_nm')
        lend_rate_type = li.get('lend_rate_type')
        lend_rate_type_nm = li.get('lend_rate_type_nm')
        
        # 금리 정보가 없는 경우 -1로 설정
        lend_rate_min = li.get('lend_rate_min', -1)
        lend_rate_max = li.get('lend_rate_max', -1)
        lend_rate_avg = li.get('lend_rate_avg', -1)

        if lend_rate_avg == None:
            lend_rate_avg = -1
        # 이미 존재하는 옵션이면 건너뛰기
        if MortgageOtions.objects.filter(
            product__fin_prdt_cd=fin_prdt_cd,
            mrtg_type=mrtg_type,
            rpay_type=rpay_type,
            lend_rate_type=lend_rate_type
        ).exists():
            continue

        save_data = {
            'fin_prdt_cd' : fin_prdt_cd,
            'mrtg_type': mrtg_type,
            'mrtg_type_nm': mrtg_type_nm,
            'rpay_type': rpay_type,
            'rpay_type_nm': rpay_type_nm,
            'lend_rate_type': lend_rate_type,
            'lend_rate_type_nm': lend_rate_type_nm,
            'lend_rate_min': lend_rate_min,
            'lend_rate_max': lend_rate_max,
            'lend_rate_avg': lend_rate_avg
        }

        serializer = MortgageOptionsSerializer(data=save_data)
        
        try:
            product = MortgageProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
            
            if serializer.is_valid(raise_exception=True):
                serializer.save(product=product)
        except MortgageProducts.DoesNotExist:
            continue

    return JsonResponse({'message': 'mortgage data save success'})

# 예금 정보 전체 조회
@api_view(['GET'])
def deposit_get_all(request):
    products = get_list_or_404(DepositProducts)
    if request.method == 'GET':
        serializer = DepositProductWithOptionSerialzier(products, many=True)
        return Response(serializer.data)
    
# 적금 정보 전체 조회
@api_view(['GET'])
def saving_get_all(request):
    products = get_list_or_404(SavingProducts)
    if request.method == 'GET':
        serializer = SavingProductWithOptionSerialzier(products, many=True)
        return Response(serializer.data)
    
# 주택담보 정보 전체 조회
@api_view(['GET'])
def mortgage_get_all(request):
    products = get_list_or_404(MortgageProducts)
    if request.method == 'GET':
        serializer = MortgageProductWithOptionSerialzier(products, many=True)
        return Response(serializer.data)
    
# 예금 정보 디테일
@api_view(["GET"])
def deposit_detail(request, pk):
    product = get_object_or_404(DepositProducts, pk=pk)
    
    if request.method == 'GET':
        serializer = DepositProductWithOptionSerialzier(product)
        return Response(serializer.data)

# 적금 정보 디테일
@api_view(["GET"])
def saving_detail(request, pk):
    product = get_object_or_404(SavingProducts, pk=pk)

    if request.method == 'GET':
        serializer = SavingProductWithOptionSerialzier(product)
        return Response(serializer.data)

# 주담대 정보 디테일
@api_view(['GET'])
def mortgage_detail(request, pk):
    product = get_object_or_404(MortgageProducts, pk=pk)

    if request.method == 'GET':
        serializer = MortgageProductWithOptionSerialzier(product)
        return Response(serializer.data)