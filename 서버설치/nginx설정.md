#### sudo nano /etc/nginx/conf.d/hizib.conf

```less
server {
    listen 80;
    server_name 192.168.0.73;

    charset utf-8;
    error_log /var/log/nginx/hizib.error.log;

    location /image {
        alias /home/hizib/image;
    }

    location / {
        if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Allow-Origin' '*';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, DELETE, PATCH, OPTIONS';
            add_header 'Access-Control-Allow-Headers' 'Content-Type, Authorization';
            add_header 'Access-Control-Max-Age' 86400;
            return 204;
        }

        add_header 'Access-Control-Allow-Origin' '*' always;
        add_header 'Content-Type' 'application/json' always;
        root /home/hizib;
        index index.html index.htm index.php;

        # 중요! PHP가 무시되지 않도록 try_files 사용
        # try_files에서 직접 lib.php를 호출하도록 수정 (밑줄 한줄 변경)
        try_files $uri $uri/ /php/library/lib.php?$args;
    
    }

    # 오류 페이지 설정
    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }

    # PHP 파일 처리
    location ~ \.php$ {
        root           /home/hizib;
        fastcgi_pass   unix:/var/run/php/php8.4-fpm.sock;
        fastcgi_index  index.php;
        fastcgi_param SCRIPT_FILENAME /home/hizib/php/library/lib.php;
        #SCRIPT_FILENAME을 lib.php로 고정(윗줄 한줄 변경)

        include        fastcgi_params;
    }

    # HTML 파일은 정적으로 제공
    location ~ \.(html|htm)$ {
        root /home/hizib;
    }
}

```

#### 기존설정 문제

⚠️ 문제 1: rewrite 때문에 PHP 파일 요청이 index.html로 무조건 리다이렉트됨
```less
if (!-e $request_filename) {
    rewrite ^(.*)$ /index.html;
}
```

⚠️ 문제 2: try_files를 사용하지 않고 if를 사용

Nginx에서 if (!-e ...) rewrite ... 패턴은 피해야 합니다. 대신 try_files를 사용해야 합니다.


#### 적용 방법

```less
sudo nginx -t              # 문법 검사

sudo systemctl reload nginx  # 설정 적용
```

#### 테스트 방법
```less
echo "<?php phpinfo(); ?>" | sudo tee /home/hizib/test.php
```

#### 브라우저 또는 Postman에서 접속
```less
http://192.168.0.73/test.php
```

#### 설정 변경 -> lib.php 연결은 됨 이후 진행해야함
```less
try_files 부분만 아래처럼 한 줄만 바꾸시면 됩니다:
try_files $uri $uri/ /php/library/lib.php?$args;

하지만 중요한 건 이게 제대로 작동하려면

location ~ \.php$ 블록에서

fastcgi_param SCRIPT_FILENAME /home/hizib/php/library/lib.php;

로 SCRIPT_FILENAME을 lib.php로 고정해주셔야 해요.

즉, try_files 한 줄 바꾸는 것 + location ~ \.php$에서 SCRIPT_FILENAME 경로 고정 이렇게 두 곳을 수정해야 문제 없이 작동합니다.
```


