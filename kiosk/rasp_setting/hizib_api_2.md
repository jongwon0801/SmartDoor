#### hizib 서버

```bash
ssh ubuntu@api.hizib.wikibox.kr  /  elcsoft

mysql -u root -p  /  위키박스
```

#### smartdoor_vod 조회, 삭제


```bash

select *from smartdoor_vod;

DELETE FROM smartdoor_vod WHERE smartdoor_vod_id = 999;

DELETE FROM smartdoor_vod;

```

#### delete
```bash
https://api.hizib.wikibox.kr/SmartdoorVod/{smartdoor_vod_id}
```
- 관리자 말고 일반 USER 로 {result : true}
- 이미 삭제 성공 시 "message": "존재하지 않는 영상 정보입니다."
- 하지만 hizib table에 바로 반영 되지않았다






