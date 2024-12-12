## Raspberry Pi Imager를 사용하여 Raspberry Pi OS 설치 
<br>
https://www.raspberrypi.com/software/

### Imager 다운 -> raspberry Pi 4 (디바이스) / raspberry Pi OS (32bit) (운영체제) / 저장소 (bootfs) 설치 

<img width="652" alt="image" src="https://github.com/user-attachments/assets/b8738cc2-e4a0-41f9-897f-7599ca578b7e">


## 전체 프로그램 업데이트 명령어

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

## 저장 단계:
- 파일 편집이 끝난 후 Ctrl+O를 누릅니다.
- 화면 하단에 File Name to Write: /etc/nginx/nginx.conf가 표시됩니다.
- Enter를 눌러 저장합니다.
- Ctrl+X를 눌러 에디터를 종료합니다.

```bash
sudo nano /etc/nginx/conf.d/localhost.conf
```

```bash
server {
        listen 80;
        server_name 127.0.0.1 localhost;

        charset utf-8;
        #access_log /var/log/nginx/host.access.log  main;

        location / {
                root /home/pi/www;
                index index.html index.htm;
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
sudo bash -c 'echo "hello world" > /home/admin/www/index.html'
```

