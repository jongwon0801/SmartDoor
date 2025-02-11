#### 버스 정류장 정보

#### 버스 정류장 코드는 네이버 지도에서 url or arrival 로 확인

```bash

sudo nano ~/www/python/config.json

# 원하는 정류장 코드 집어 넣는다
"isUseBus":true, "busRefresh":60,  "busStopes":["93583","93582"], 

```

#### 날씨 수정 (네이버 날씨의 url 에서 code 확인가능)

- 단지 정보 areacode 수정 put method (관리자만 가능)

```bash

https://api.hizib.wikibox.kr/SmartdoorGroup/{smartdoor_group_id}

{
  "areacode": "01110675",
  "name": "양양양양",
  "address": {
    "zipcode": "08510",
    "addressMain": "양양군11"
  }
}

```
#### 수정 후 sudo reboot 하면 적용됨


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
