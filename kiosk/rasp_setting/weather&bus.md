#### 버스 정류장 정보

```bash

sudo nano ~/www/python/config.json

# 원하는 정류장 코드 집어 넣는다
"isUseBus":true, "busRefresh":60,  "busStopes":["93583","93582"], 

```

#### 날씨 데이터 api (관리자만 가능)

```bash

서울특별시 금천구 가산동
https://api.hizib.wikibox.kr/Weather/areacode?keyword=
%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C%20%EA%B8%88%EC%B2%9C%EA%B5%AC%20%EA%B0%80%EC%82%B0%EB%8F%99

```

#### 날씨데이터

#### ubuntu@api.hizib.wikibox.kr 서버의
- smartdoor_group 의 areacode 컬럼 코드 이용
- weather 테이블에 해당 지역의 areacode로 날씨데이터 가져옴

```bash


1. 처음 기기 serial number를 등록하면 서버의 weather 테이블에서 smartdoor 테이블에있는 smartdoor_group_id, code 이용

2. 해당 하는 smartdoor의 code로 smartdoor_group_id를 조회

3. smartdoor_group 테이블에서 smartdoor_group_id를 통해 areacode 조회

4. weather 테이블에서 areacode 로 저장된 날씨데이터 가져옴

5. local DB hizib의 weather 테이블에 저장, smartdoor 테이블에 스마트도어 정보 저장




```
