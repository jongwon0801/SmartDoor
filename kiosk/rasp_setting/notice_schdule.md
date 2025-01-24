
```bash
# smartdoor_notice_id 82인 레코드 삭제
DELETE FROM smartdoor_notice WHERE smartdoor_notice_id = 82;

# smartdoor_schedule_id 1, 2 레코드 삭제
DELETE FROM smartdoor_schedule WHERE smartdoor_schedule_id IN (1, 2);

# smartdoor_schedule_id 1, 2가 아닌 레코드 삭제
DELETE FROM smartdoor_schedule WHERE smartdoor_schedule_id NOT IN (1, 2);

# smartdoor_notice 테이블에서 smartdoor_notice_id가 2인 레코드를 제외한 나머지 레코드를 삭제
DELETE FROM smartdoor_notice WHERE smartdoor_notice_id <> 2;

```
#### 공지사항

- 공지사항은 서버 smartdoor_notice 테이블에서 레코드를 삭제하고 로컬 디비에만 레코드가 남아있으면
키오스크 화면에는 로컬 디비의 저장된걸 보여줌

- 공지사항을 앱으로 작성하면 서버의 디비에 레코드 추가 되고 로컬디비에 값이 추가됨
- 
```bash
app 에서 공지사항 목록은 서버 디비에서 조회해서 가져온다

키오스크화면은 로컬 디비의 값을 보여줌

공지사항 로컬 디비 값을 삭제해도 키오스크 실시간 반영안됨
(새로 공지사항을 추가할때 키오스크 화면에 반영된다)
```

#### 스케줄

- 스케줄 smartdoor_schedule 서버 테이블에 레코드 추가 하면 로컬디비에도 추가됨

- smartdoor_schedule 일정을 서버 디비에서 삭제 하면 로컬디비엔 데이터 남아있지만
앱 목록 에서는 서버의 스케줄을 표시함

- smartdoor_schedule 로컬 디비 테이블 내용 삭제해도 앱 목록 에는 서버 데이터를 가져옴

```bash
스케줄 목록은 서버에서 데이터를 가져온다 (서버에서가져온다 -> 서버 테이블 수정하면 APP 목록내용 바뀜)
하지만 키오스크 화면은 로컬 db에서 값을 가져오기 때문에  서버에서 디비 수정해도 안바뀜
```

#### hizib 데이터베이스 생성
- create database hizib;


