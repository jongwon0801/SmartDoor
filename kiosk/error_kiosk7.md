
### nginx websocket 설정 변경

```bash

server {
    listen 80;
    server_name 127.0.0.1 localhost;

    charset utf-8;

    location / {
        root /home/pi/www;
        index index.html index.htm;
    }

    location ^~ /ws/ {
        # proxy_pass 경로에서 /ws/ 경로가 그대로 전달되도록 수정
        proxy_pass http://127.0.0.1:8080/;

        # WebSocket을 지원하기 위한 설정
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }

    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }
}






```
