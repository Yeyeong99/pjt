# 06_pjt: 금융
## Todo
- finlife 앱에 DepositProduct => 외래키 용으로 만들어둔 거라 지워야
- serializer에 읽기 전용 추가
### utils.py : 전처리
데이터 가져오고 전처리(형변환)=> view로 보내서 => serializers 로 vaild 해서 저장

- products
  - join_deny: 가입 제한 => int로 형변환 필요
  - etc_note, spcl_cnd: \n ※ 같은 거 없애야함 (금융 상품 설명) => [0-9, 가-힣] 이런 식으로 정규표현식을 통해 포함되어야 하는 문자만 필터링하기
  - join_way: "인터넷,스마트폰"
    - 여러 방법이 써있는 경우: 하나의 텍스트로 그대로 저장
- option 
  - "save_trm": "1" => integer
  - 조건에 맞는 필드만 가져오기