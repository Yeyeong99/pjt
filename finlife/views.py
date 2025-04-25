from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .utils import preprocessing
from .serializers import DepositProductSerializer
from .models import DepositOptions, DepositProducts
from .utils import format_option_list
from .serializers import DepositOptionSerializer
import requests
from django.conf import settings


# Create your views here.
@api_view(['GET'])
def save_deposit_products(request):
    products = preprocessing('020000')
    for product in products:
        serializer = DepositProductSerializer(data=product)
        if serializer.is_valid(raise_exception=True):
            serializer.save()



url = f"http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={settings.API_KEY}&topFinGrpNo=020000&pageNo=1"

response = requests.get(url)

# 정기 예금 상품 목록 데이터를 가져와서 정기 예금의 상품 목록과 옵션 목록을 DB에 저장
api_view(['GET'])
def save_depsoit_products(request):
    options = response.json()['result']['optionList']
    for option in options:
        formatted_option = format_option_list(option)
        product = DepositProducts.objects.get(product_code=formatted_option['fin_prdt_cd'])
        formatted_option['product'] = product
        serializer = DepositOptionSerializer(formatted_option)
        if serializer.is_valid():
            serializer.save(product=product)


# 특정 상품의 옵션 리스트 반환
api_view(['GET'])
def deposit_product_options(request, fin_prdt_cd):
    options = DepositOptions.objects.filter(fin_prdt_cd=fin_prdt_cd)
    serializer = DepositOptionSerializer(options, many=True)
    return Response(serializer.data)

# 가입 기간에 상관없이 금리가 가장 높은 상품과 해당 상품의 옵션 리스트 출력
api_view(['GET'])
def top_rate(request):
    # 가장 높은 금리인 옵션을 통해 가장 높은 금리 찾기
    highest_rate_option = DepositOptions.objects.all().order_by('-intr_rate2').first()
    # 가장 높은 금리 옵션을 이용해 프로덕트 찾기
    product = DepositProducts.options.get(id=highest_rate_option.product)
    # 프로덕트의 옵션 리스트
    product_options = DepositOptions.objects.filter(product=product)

    # product, 옵션 리스트 serializer
    serializer_options = DepositOptionSerializer(product_options, many=True)

    data = {
        'serializer_options': serializer_options,
    }

    return Response(data)


@api_view(['GET', 'POST'])
def deposit_products(request):
    if request.method == 'GET':
        deposit_product_list = DepositProducts.objects.all()
        serializer = DepositOptionSerializer(deposit_product_list, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = DepositOptionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)