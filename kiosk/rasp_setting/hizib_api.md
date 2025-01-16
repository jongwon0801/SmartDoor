#### hizib 서버

```bash
ssh ubuntu@api.hizib.wikibox.kr  /  elcsoft

mysql -u root -p  /  위키박스
```

#### mysql 테이블 조회

#### smartdoor_user table column
- smartdoor_user_id (초대, 첫기기등록으로 기기가 배정된 계정)
- user_id (회원가입한 계정), isOwner (소유자 여부 1), smartdoor_id (스마트도어의 아이디)

```bash
# 기기 등록한 계정 조회
select *from smartdoor_user;

# 전체 user 정보 조회
select *from user;

# 전체 스마트도어 조회
select *from smartdoor;

# 관리자 계정 조회
select *from admin;

# 스마트도어 그룹 조회
select *from smartdoor_group;
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

#### 2. 관리자 등록 (FM은 관리자 admin 하나만 씀 연습용으로 만듬)

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
# 스마트도어 기기 등록은 관리자 계정 아니어도 가능, 로그인은 해야함
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

#### 5. 스마트 도어 오너 등록

```bash
# 어플에서 QR 코드로 기기 등록을 하면 최초로 등록한 유저가 Owner 된다
# 이후 유저들은 QR 등록 불가능 / 오너가 초대로만 유저등록 가능

# post
https://api.hizib.wikibox.kr/SmartdoorUserInvite

{
  "name": "이름이름",
  "handphone": "010-1234-2222"
}

# 처음 초대 api 보내면 smartdoor_user 테이블에 입력안됨
# 어플로 초대한 계정 로그인 성공 하면 smartdoor_user 테이블에 초대한 계정 추가됨
# fcm_token은 이유는 모르겠지만 비워둬도 나중에 자동으로 추가됨 (스마트도어 초대받아서 등록한 이후)


```
