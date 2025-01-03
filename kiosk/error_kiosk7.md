
### nginx websocket 설정 변경

```bash

server {
    listen 80;
    server_name 127.0.0.1 localhost;

    charset utf-8;

    # 일반 HTTP 요청을 처리하는 설정
    location / {
        root /home/pi/www;
        index index.html index.htm;
    }

    # WebSocket 요청을 처리하는 설정
    location ^~ /ws/ {
        # /ws/ 경로를 그대로 전달하기 위한 rewrite 설정
        rewrite ^/ws/(.*)$ /ws/$1 break;

        # Tornado 서버로 WebSocket 요청을 전달
        proxy_pass http://127.0.0.1:8080/ws/$1;

        # WebSocket을 위한 헤더 설정
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }

    # 서버 오류 페이지 설정
    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }
}

```

### nginx 재시작

```bash

sudo systemctl reload nginx



```







