from rest_framework import serializers
from .models import DepositProducts, DepositOptions

# 금융 상품 직렬화 시리얼라이저
class DepositProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProducts
        fields = '__all__'


class DepositOptionSerializer(serializers.ModelSerializer):
    # product : 읽기 전용으로 추가해야함
    class Meta:
        model = DepositOptions
        fields = '__all__'