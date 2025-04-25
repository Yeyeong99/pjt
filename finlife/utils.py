import requests
import json
import re

from django.conf import settings

# API_KEY = '7ac2fed38f15fcc85ba028f86ca2010f'

# 요청 URL (base)
BASE_URL = 'http://finlife.fss.or.kr/finlifeapi/'

def get_fin_product_data(fin_company_code):
    # 정기예금 요청 URL
    URL = BASE_URL + 'depositProductsSearch.json'
    params = {
        'auth': settings.API_KEY,
        # 원하는 금융회사 코드 넣기
        'topFinGrpNo': fin_company_code,
        'pageNo': 1
    }
    response = requests.get(URL, params=params).json()
    products = response['result']['baseList']

    # 원하는 필드만 추출하기기
    extracted = []
    for product in products:

        new_fields = {}
        for key in product.keys():
            if key in ['fin_prdt_cd', 'kor_co_nm', 'fin_prdt_nm', 'etc_note', 'join_deny', 'join_member', 'join_way', 'spcl_cnd']:
                new_fields[key] = product.get(key, '')
        extracted.append(new_fields)

    return extracted

# extracted_products = get_fin_product_data('020000')

# 전처리
def preprocessing(fin_company_code):

    extracted_products = get_fin_product_data(fin_company_code)
    
    for product in extracted_products:
        if 'join_deny' in product:
            product['join_deny'] = int(product['join_deny'])    # 정수 변환

        if 'etc_note' in product:
            text = product['etc_note'].replace('\n', '')
            new_text = re.sub(r'[^a-zA-Z가-힣%\s]', '', text)
            product['etc_note'] = new_text

        if 'spcl_cnd' in product:
            text = product['etc_note'].replace('\n', '')
            new_text = re.sub(r'[^a-zA-Z가-힣%\s]', '', text)
            product['etc_note'] = new_text

    result_string = json.dumps(extracted_products)
    result = json.loads(result_string)
    
    return result

def format_option_list(option):
    option_dict = {}
    for key in option:
        if key not in ('dcls_month', 'fin_co_no', 'intr_rate_type'):
            if key == 'save_trm':
                option_dict[key] = int(option[key])
            else:
                option_dict[key] = option[key]


    return option_dict
