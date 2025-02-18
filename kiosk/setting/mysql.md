#### mysql 설치, 등록

```bash

sudo apt-get install mariadb-server

sudo mysql -u root
set password for root@'localhost'=PASSWORD('dnlzlqkrtm');

# 권한 적용
# FLUSH PRIVILEGES -> 디스크에 저장된 사용자 권한 테이블(mysql.user, mysql.db, 등)의 내용을 다시 읽어서 메모리 캐시에 로드
# 사용자 권한 정보의 캐시를 초기화하고 업데이트하는 역할
FLUSH privileges;

create database hizib;
exit

```


#### mysql 진입

```bash

mysql -u root -p

password : dnlzlqkrtm

```

#### 데이터 베이스 조회
```bash

SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| hizib              |
| information_schema |
| mysql              |
| performance_schema |
+--------------------+
hizib 빼고는 기본으로 생성됨

USE hizib;

SHOW TABLES;

# pymysql 패키지 경로
ls /home/pi/.virtualenvs/elcsoft/lib/python3.9/site-packages/pymysql


```

#### hizib database 삭제 후 초기화면 만들기

```bash

DROP DATABASE hizib;

# hizib 다시 생성
sudo mysql -u root

set password for root@'localhost'=PASSWORD('dnlzlqkrtm');

FLUSH privileges;

create database hizib;
exit

# webserver 재실행
sudo systemctl daemon-reload

sudo systemctl enable tornado.service

sudo systemctl start tornado.service

sudo systemctl status tornado.service



```
