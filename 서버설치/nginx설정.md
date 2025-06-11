#### sudo nano /etc/nginx/conf.d/hizib.conf

```less
server {
    listen 80;
    server_name api1.hizib.wikibox.kr;

    charset utf-8;
    #access_log  /var/log/nginx/hizib.access.log  main;
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
        if (!-e $request_filename) {
                rewrite ^(.*)$ /index.html;
        }
    }

    #error_page 404 /404.html;


    # redirect server error pages to the static page /50x.html
    #
    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }

    location ~ \.(php|html|htm)$ {
        root           /home/hizib;
        fastcgi_pass   unix:/var/run/php/php7.4-fpm.sock;
        fastcgi_index  index.html;
        fastcgi_param  SCRIPT_FILENAME  $document_root$fastcgi_script_name;
        include        fastcgi_params;
        #include snippets/fastcgi-php.conf;
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
http://api1.hizib.wikibox.kr/test.php
```




