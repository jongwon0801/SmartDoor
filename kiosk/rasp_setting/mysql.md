#### mysql 설치, 등록

```bash

sudo apt-get install mariadb-server

sudo mysql -u root
set password for root@'localhost'=PASSWORD('dnlzlqkrtm');
# 권한 적용
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

DROP DATABASE hizib;

# pymysql 패키지 경로
ls /home/pi/.virtualenvs/elcsoft/lib/python3.9/site-packages/pymysql




```
