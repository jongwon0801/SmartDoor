#### hizib 서버

```bash
ssh ubuntu@api.hizib.wikibox.kr  /  elcsoft

mysql -u root -p  /  위키박스
```

#### mysql 테이블 조회

```bash
# 스마트도어 유저정보 smartdoor_user_id, smartdoor_id, user_id, isOwner, smartdoor_id, 
select *from smartdoor_user;

# 전체 user 정보 조회
select *from user;

# 전체 스마트도어 조회
select *from smartdoor;

```

#### 1. 회원 가입

```bash
# post
https://api.hizib.wikibox.kr/user

# body
{
  "id": "cjw111",
  "passwd": "1234",
  "repasswd": "1234",
  "name": "종원",
  "nickname": "종1",
  "ci": "",
  "handphone": "010-1234-123",
  "email": "test@test.com",
  "isUse": 1
}

```

#### 2. 관리자 등록

```bash
# post
# 이전에 등록된 관리자 admin 계정으로 토큰 받아야함 (관리자가 admin table 에 하나도 없으면 로그인 하지 않고 등록 가능)
# https://api.hizib.wikibox.kr/admin/login 로그인 해서 토큰을 받고
# 해당 토큰 헤더에 넣고 https://api.hizib.wikibox.kr/admin

{
  "id": "jongwon",
  "passwd": "1234",
  "repasswd": "1234",
  "name": "jongwon",
  "handphone": "010-5555-6666",
  "email": "wemaster@hizib.com"
}


```

#### 3. 스마트 도어 단지 등록

```bash
# post
# /admin/login 에서 새로 등록한 관리자 토큰 으로 그룹 생성 (관리자 권한 필요)
# https://api.hizib.wikibox.kr/SmartdoorGroup

{
  "areacode": "12345678",
  "name": "테스트1",
  "address": {
    "zipcode": "12345",
    "addressMain": "테스트공간"
  }
}


```

#### 4. 스마트 도어 기기 등록

```bash
# post
# 단지가 존재하지 않으면 "message": "존재하지 않는 단지 정보입니다."
# https://api.hizib.wikibox.kr/Smartdoor

{
  "smartdoor_group_id": 8,
  "code": "12345678",
  "name": "뉴비",
  "dong": "",
  "ho": "111",
  "status": 1
}



```
