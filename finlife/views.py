from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .utils import preprocessing
from .serializers import DepositProductSerializer
from .models import DepositOptions, DepositProducts
from .serializers import DepositOptionSerializer


# Create your views here.
@api_view(['GET'])
def save_deposit_products(request):
    products, options = preprocessing('020000')
    for product in products:
        serializer = DepositProductSerializer(data=product)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
    for option in options:
        product = DepositProducts.objects.get(fin_prdt_cd=option['fin_prdt_cd'])
        option['product'] = product.id
        serializer = DepositOptionSerializer(data=option)
        if serializer.is_valid():
            serializer.save(product=product)

    return Response({'save': 'completed'}, status=status.HTTP_202_ACCEPTED)


# 특정 상품의 옵션 리스트 반환
@api_view(['GET'])
def deposit_product_options(request, fin_prdt_cd):
    options = DepositOptions.objects.filter(fin_prdt_cd=fin_prdt_cd)
    serializer = DepositOptionSerializer(options, many=True)
    data = {
        'serializer_options': serializer.data,
    }
    return Response(data)

# 가입 기간에 상관없이 금리가 가장 높은 상품과 해당 상품의 옵션 리스트 출력
@api_view(['GET'])
def top_rate(request):
    # 가장 높은 금리인 옵션을 통해 가장 높은 금리 찾기
    highest_rate_option = DepositOptions.objects.all().order_by('-intr_rate2').first()
    # 가장 높은 금리 옵션을 이용해 프로덕트 찾기
    product = DepositProducts.objects.get(id=highest_rate_option.product_id)
    
    # 프로덕트의 옵션 리스트
    product_options = DepositOptions.objects.filter(product=product)
    # product, 옵션 리스트 serializer
    serializer_options = DepositOptionSerializer(product_options, many=True)
    product_serializer = DepositProductSerializer(product)

    data = {
        'product':product_serializer.data,
        'options': serializer_options.data,
    }

    print(data)
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def deposit_products(request):
    if request.method == 'GET':
        deposit_product_list = DepositProducts.objects.all()
        serializer = DepositProductSerializer(deposit_product_list, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = DepositProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)