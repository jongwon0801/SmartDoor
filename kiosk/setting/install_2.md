### nginx 설치

```bash

sudo apt-get install nginx

sudo nano /etc/nginx/nginx.conf

# 이유 : 클라이언트가 전송하는 데이터 크기를 제한하지 않아서 대용량 파일 업로드나 특정 상황에서 데이터를 제한 없이 전송할 수 있도록 하기 위해서
http {
	client_max_body_size 0;
}

include /etc/nginx/conf.d/*.conf;
include /etc/nginx/sites-enabled/*;


sudo nano /etc/nginx/conf.d/localhost.conf

이유 : HTTP 요청과 WebSocket 요청을 처리하는 웹 서버를 설정

sudo systemctl restart nginx

sudo service nginx restart

```

#### localhost.conf 생성, 내용 추가

#### mariadb 설치

```less
sudo apt-get install mariadb-server

sudo mysql -u root

set password for root@'localhost'=PASSWORD('dnlzlqkrtm');

flush privileges;

create database hizib;

SHOW DATABASES;

USE hizib;

exit

```

#### 데이터 베이스 삭제
```less
DROP DATABASE hizib;
```




