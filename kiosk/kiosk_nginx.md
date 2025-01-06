


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

### /etc/nginx/nginx.conf 설정

```bash
sudo nano /etc/nginx/nginx.conf

http {
	client_max_body_size 0;
}
```
- client_max_body_size 0; 설정은 NGINX 서버에서 클라이언트 요청의 본문(body) 크기에 대한 최대 허용 크기를 0으로 설정
- 요청 본문 크기 제한을 완전히 제거하는 설정. 요청 본문 크기에 제한이 없어져, 큰 파일 업로드와 같은 경우에 크기 제한 없이 데이터를 받기 가능


### nano 편집기 저장
- 파일 편집이 끝난 후 Ctrl+O를 누릅니다.
- 화면 하단에 File Name to Write: /etc/nginx/nginx.conf가 표시됩니다.
- Enter를 눌러 저장합니다.
- Ctrl+X를 눌러 에디터를 종료합니다.


## localhost.conf 파일 생성
```bash
sudo nano /etc/nginx/conf.d/localhost.conf
```

- NGINX가 어떤 설정을 사용할지는 설정 파일의 우선순위에 따라 결정됩니다.
- 특히 server_name과 listen 지시어가 중요한 역할을 합니다.


- 80 포트로 접속할 때:
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
```bash

1. listen 80;
Nginx가 HTTP 프로토콜을 사용하여 80번 포트에서 요청을 수신하도록 설정합니다. 이는 웹 서버가 기본적으로 사용하는 포트입니다.

2. server_name 127.0.0.1 localhost;
서버의 이름을 지정합니다. 여기서는 127.0.0.1 (로컬호스트 IP 주소)와 localhost로 설정되어 있습니다. 이를 통해 서버가 이 이름들로 접근되는 요청을 처리합니다.

3. charset utf-8;
서버가 처리하는 모든 응답에 대해 UTF-8 문자 인코딩을 사용하도록 지정합니다. 이는 웹 페이지에서 다양한 언어의 문자를 올바르게 표시할 수 있게 합니다.

4. location / { ... }
/ 경로에 대한 요청을 처리하는 설정입니다. 기본적으로 요청된 파일을 /home/pi/www 디렉터리에서 찾고, index.html 또는 index.htm 파일을 기본 페이지로 제공합니다.
즉, 웹 브라우저에서 http://127.0.0.1/로 접근하면 해당 디렉터리에 있는 기본 파일을 반환합니다.

5. location ^~ /ws/ { ... }
/ws/로 시작하는 경로에 대한 요청을 처리하는 설정입니다. 여기서는 WebSocket 프로토콜을 처리하려는 것으로 보입니다.
rewrite ^/ws/(.*)$ /ws/$1 break;: /ws/ 이후의 경로를 그대로 유지하면서 리다이렉트합니다.
proxy_pass http://127.0.0.1:8080/ws/$1;: /ws/로 시작하는 요청을 로컬 서버의 8080번 포트로 전달합니다.
이를 통해 Nginx가 WebSocket 서버와의 프록시 역할을 하게 됩니다.
proxy_http_version 1.1;, proxy_set_header upgrade $http_upgrade;, proxy_set_header Connection "upgrade";: WebSocket 연결이 성공적으로 이루어지도록 필요한 HTTP 헤더를 설정합니다. WebSocket은 HTTP/1.1을 사용하며, upgrade 헤더가 필요합니다.
proxy_set_header Host $host;: 요청 헤더의 Host 값을 원래의 요청과 동일하게 설정합니다. 이는 백엔드 서버가 요청을 올바르게 처리할 수 있도록 돕습니다.

6. error_page 500 502 503 504 /50x.html;
서버에서 500번대 에러가 발생했을 때 사용자에게 보여줄 페이지를 설정합니다. 이 경우, 서버 오류 페이지가 /50x.html로 설정됩니다.
location = /50x.html { root /usr/share/nginx/html; }: 이 페이지를 /usr/share/nginx/html 디렉터리에서 찾습니다.

요약
이 Nginx 설정은 HTTP 요청과 WebSocket 요청을 처리하는 웹 서버를 설정한 것입니다. 기본적으로 로컬에서 서비스되는 웹 페이지를 제공하며, /ws/로 시작하는 요청은 로컬의 8080번 포트로 전달하여 WebSocket 연결을 처리합니다. 추가적으로 500번대 오류가 발생했을 때 사용자에게 오류 페이지를 보여주는 설정도 포함되어 있습니다.


```


### 디렉토리 생성
지정한 경로(/home/pi/www)가 없다면 먼저 디렉토리를 생성해야 합니다.

```bash
sudo mkdir -p /home/pi/www
```

- -p 옵션은 중간 디렉토리가 없는 경우 함께 생성합니다.
- 디렉토리가 생기면 현재 설정한 Nginx의 root 디렉토리가 됩니다.


### /home/admin/www 경로에 index.html 작성
```bash
sudo nano /home/pi/www/index.html
```

```bash
sudo bash -c 'echo "hello world" > /home/pi/www/index.html'
```

### 권한 설정
Nginx가 파일에 접근할 수 있도록 디렉토리 및 파일 권한을 설정합니다.

```bash
sudo chmod -R 755 /home/pi/www
sudo chown -R www-data:www-data /home/pi/www
```

www-data는 Nginx가 사용하는 기본 사용자/그룹입니다.

- 웹 요청 처리
브라우저를 통해 웹 페이지를 요청하면, 웹 서버(Apache/Nginx)가 해당 요청을 처리하며, 이때 www-data 사용자의 권한으로 파일에 접근합니다. 웹 서버 외에는 www-data 권한을 가진 다른 사용자가 없도록 설정하는 것이 일반적입니다.

- 제한된 사용자
기본적으로 리눅스의 보안 설계는 www-data 사용자가 시스템의 다른 파일이나 디렉토리에 접근하지 못하도록 제한합니다.
예: /etc나 /home 같은 중요한 디렉토리에는 www-data가 접근할 수 없습니다.

1. Nginx는 /etc/nginx/nginx.conf를 먼저 읽습니다.
2. include /etc/nginx/conf.d/*.conf; 디렉티브에 따라 /etc/nginx/conf.d/ 디렉토리에 있는 파일들을 읽어 추가 설정을 병합합니다.
3. /etc/nginx/conf.d/localhost.conf와 같은 파일이 포함되면, 그 내용은 nginx.conf의 일부처럼 동작합니다.


