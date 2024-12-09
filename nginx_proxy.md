# Nginx Proxy 설정

## `/googlehome` 경로 설정
`location /googlehome {}`  
- `/googlehome` 경로로 들어오는 요청을 처리하는 블록입니다.  
- 사용자가 `http://your-domain.com/googlehome`으로 요청을 보내면, 이 블록의 내용에 따라 처리됩니다.

```nginx
location /googlehome {
    proxy_pass http://127.0.0.1:5000/;  # Flask 서버의 /googlehome 엔드포인트로 전달
    # Flask 서버는 127.0.0.1(localhost)에서 포트 5000으로 실행 중
}
```

### 이 설정은 요청을 Nginx에서 처리하지 않고 Flask의 /googlehome 엔드포인트로 직접 프록시합니다.
### 중요: Nginx의 /googlehome과 Flask의 /googlehome이 중첩되지 않도록 조심해야 합니다.

```
proxy_set_header
클라이언트의 요청 정보를 Flask 서버에 전달하거나 수정할 때 사용합니다.

Host $host:
원래 클라이언트가 요청한 도메인(호스트 이름)을 전달합니다.
Flask 서버는 이 헤더를 사용하여 요청의 출처를 알 수 있습니다.

X-Real-IP $remote_addr:
클라이언트의 실제 IP 주소를 전달합니다.
Flask 서버는 클라이언트의 원래 IP를 로그에 기록하거나 요청의 출처를 식별할 수 있습니다.

X-Forwarded-For $proxy_add_x_forwarded_for:
클라이언트의 IP 주소 및 요청이 거친 프록시 서버의 IP 주소 목록을 전달합니다.
여러 프록시를 거친 요청일 경우 유용합니다.

X-Forwarded-Proto $scheme:
클라이언트가 요청한 프로토콜(HTTP 또는 HTTPS)을 전달합니다.
Flask가 요청이 안전한 HTTPS 연결을 통해 이루어졌는지 확인하는 데 사용됩니다.
```


## /etc/nginx/conf.d 경로에 hizib.conf 에 location 추가 Virtual derectory

```nginx
location /googlehome {
        proxy_pass http://127.0.0.1:5000/googlehome;  # Flask의 /googlehome으로 직접 전달
        proxy_set_header Host $host;
     #   proxy_set_header X-Real-IP $remote_addr;
     #   proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
     #   proxy_set_header X-Forwarded-Proto $scheme;
    }
```
