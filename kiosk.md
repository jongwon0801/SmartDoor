## Raspberry Pi Imager를 사용하여 Raspberry Pi OS 설치 
<br>
https://www.raspberrypi.com/software/

### Imager 다운 -> raspberry Pi 4 (디바이스) / raspberry Pi OS (32bit) (운영체제) / 저장소 (bootfs) 설치 

<img width="652" alt="image" src="https://github.com/user-attachments/assets/b8738cc2-e4a0-41f9-897f-7599ca578b7e">


### 전체 프로그램 업데이트 명령어

```bash
1. 캐시 정리
sudo apt clean

2. 사용하지 않는 패키지 제거
sudo apt autoremove -y

3. 패키지 목록 업데이트
sudo apt update

4. 시스템 패키지 업그레이드
sudo apt upgrade
```


### nginx 설치

```bash
sudo apt-get install nginx
```

### nginx 설정

```bash
sudo nano /etc/nginx/nginx.conf

http {
	client_max_body_size 0;
}
```
### client_max_body_size 0; 설정은 NGINX 서버에서 클라이언트 요청의 본문(body) 크기에 대한 최대 허용 크기를 0으로 설정
### 요청 본문 크기 제한을 완전히 제거하는 설정. 요청 본문 크기에 제한이 없어져, 큰 파일 업로드와 같은 경우에 크기 제한 없이 데이터를 받기 가능


### nano 편집기 저장
- 파일 편집이 끝난 후 Ctrl+O를 누릅니다.
- 화면 하단에 File Name to Write: /etc/nginx/nginx.conf가 표시됩니다.
- Enter를 눌러 저장합니다.
- Ctrl+X를 눌러 에디터를 종료합니다.


## localhost.conf 파일 생성
```bash
sudo nano /etc/nginx/conf.d/localhost.conf
```

NGINX가 어떤 설정을 사용할지는 설정 파일의 우선순위에 따라 결정됩니다.
특히 server_name과 listen 지시어가 중요한 역할을 합니다.

시나리오:
80 포트로 접속할 때:

/etc/nginx/conf.d/localhost.conf 파일에 설정된 server 블록이 작동합니다.
이유:
server_name이 127.0.0.1 및 localhost로 지정되어 있고, listen 80;이 명시되어 있기 때문입니다.
/etc/nginx/sites-available/default로 가지 않음:

server_name이 localhost.conf와 충돌하지 않는 한, localhost.conf 설정이 우선 적용됩니다.
만약 default 파일에도 동일한 server_name이 설정되어 있다면, 가장 먼저 로드된 설정이 적용됩니다(주로 /etc/nginx/conf.d/*.conf가 우선).


```bash
server {
        listen 80;
        server_name 127.0.0.1 localhost;

        charset utf-8;
        #access_log /var/log/nginx/host.access.log  main;

        location / {
                root /home/admin/www;
                index index.html;
        }

        location ^~ /ws/ {
                rewrite ^/ws/(.*)$ /ws/$1 break;
                proxy_pass http://127.0.0.1:8080/ws/$1;
                proxy_http_version      1.1;
                proxy_set_header        upgrade $http_upgrade;
                proxy_set_header        Connection "upgrade";
                proxy_set_header        Host $host;
        }

        #error_page 404 /404.html;

        # redirect server error pages to the static page /50x.html
        #
        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
                root /usr/share/nginx/html;
        }
}

```

## /home/admin/www 경로에 index.html 작성

```bash
sudo bash -c 'echo "hello world" > /home/admin/www/index.html'
```

