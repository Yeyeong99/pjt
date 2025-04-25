from django.db import models

# Create your models here.
class DepositProducts(models.Model):
    JOIN_WAY_CHOICES = [
        (1, '제한없음'),
        (2, '서민전용'),
        (3, '일부제한'),
    ]

    fin_prdt_cd = models.TextField(unique=True)
    kor_co_nm = models.TextField()
    fin_prdt_nm = models.TextField()
    etc_code = models.TextField(null=True, blank=True)
    join_deny = models.IntegerField(choices=JOIN_WAY_CHOICES,
                                    default=1)
    join_member = models.TextField()
    join_way = models.TextField()
    spcl_cnd = models.TextField()


class DepositOptions(models.Model):
    product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE, related_name='options')
    fin_prdt_cd = models.TextField()  # 금융 상품 코드
    intr_rate_type_nm = models.CharField(max_length=100)  # 저축금리 유형명
    intr_rate = models.FloatField()  # 저축 금리
    intr_rate2 = models.FloatField()  # 최고 우대 금리
    save_trm = models.IntegerField()  # 저축 기간 (단위: 개월)
